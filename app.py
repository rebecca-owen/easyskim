import os
from urlparse import urlsplit, urlunsplit
import tempfile
from subprocess import check_output
import json

import urllib
from flask import Flask, redirect, render_template, request, session
from mendeley import Mendeley
from mendeley.session import MendeleySession
from werkzeug.contrib.fixers import ProxyFix

import wrapper
import codecs

import jinja_filters

def getSecrets():
    config_file = 'app.json'
    if os.path.exists(config_file):
        with open(config_file) as f:
            config = json.load(f)
            c_id = config['env']['MENDELEY_CLIENT_ID']['description']
            c_secret = config['env']['MENDELEY_CLIENT_SECRET']['description']
            c_debug = config['env']['DEBUG']
            return c_id, c_secret, c_debug
    c_id = os.environ.get('MENDELEY_CLIENT_ID')
    c_secret = os.environ.get('MENDELEY_CLIENT_SECRET')
    c_debug = os.getenv('EASYSKIM_DEBUG', True)
    if c_id and c_secret:
        return c_id, c_secret, c_debug
    raise Exception('Mendeley client id and secret not found in configuration')

client_id, client_secret, debug = getSecrets()

app = Flask(__name__)
app.jinja_env.filters['authors'] = jinja_filters.authors
app.debug = debug
app.secret_key = client_secret
app.wsgi_app = ProxyFix(app.wsgi_app)


@app.route('/')
def login():
    return render_template('login.html')


@app.route('/oauth')
def oauth():
    mendeley = get_mendeley_config()
    auth = mendeley.start_authorization_code_flow(state=session['state'])
    mendeley_session = auth.authenticate(request.url)

    session.clear()
    session['token'] = mendeley_session.token

    return redirect('/home')


@app.route('/home')
def home():
    if 'token' in session:
        # return redirect('/')

        mendeley_session = get_session_from_cookies()

        name = mendeley_session.profiles.me.display_name
        docs = []
        if mendeley_session.documents:
            for document in mendeley_session.documents.iter():
                temp_dict = {
                        'title': document.title,
                        'id': document.id,
                    }
                if document.authors:
                    temp_dict['names'] = ['%s, %s' % (x.last_name, x.first_name) for x in document.authors]
                else:
                    temp_dict['names'] = []
                docs.append(temp_dict)

        context = {
            'name' : mendeley_session.profiles.me.display_name,
            'docs': docs[:5],
            'logged_in': True
        }
    else:
        mendeley = get_mendeley_config()
        auth = mendeley.start_authorization_code_flow()
        session['state'] = auth.state

        context = {'login_url':auth.get_login_url()}
    return render_template('home.html', **context)

@app.route('/document', methods=['POST'])
def document():
    if 'token' not in session:
        return json.dumps({ "error": "not logged in" }), 500

    mendeley_session = get_session_from_cookies()

    doc_id = request.form['doc_id']
    raw_text, metadata = convertToTxt(getPdf(mendeley_session, doc_id))
    text = wrapper.textChanger(textToEncoded(raw_text))

    return json.dumps({ "text": text }), 200

# def getMeta(session, data):
#     data = json.loads(data)
#     doi = data['DOI']
#     print doi
#     author = data['Author']
#     print author
#     # html = '<p>Number of Mendeley Readers: ' + session.catalog.by_identifier(doi=doi, view='stats').reader_count + '</p>'
#         # +'<p>Other Papers by Author in Catalogue: ' + session.catalog.advanced_search(author=Author) + '</p>'
#         # +'<p>Full citation: ' + session.catalog.by_identifier(doi, view='bib') + '</p>'
#     html = ""
#     return html

@app.route('/static/<path:path>')
def static_proxy(path):
    # send_static_file will guess the correct MIME type
    return app.send_static_file(os.path.join('static', path))

@app.route('/logout')
def logout():
    session.pop('token', None)
    return redirect('/home')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] == 'pdf'

@app.route('/uploaded', methods=['POST'])
def uploaded_file():
    temp = request.files['file']
    if temp and allowed_file(temp.filename):
        f = tempfile.NamedTemporaryFile(delete=False)
        f.write(temp.stream.read())
        f.close()
        raw_text, metadata = convertToTxt(f)
        text = wrapper.textChanger(textToEncoded(raw_text))
        return json.dumps({ "text": text, "meta": metadata }), 200
    return json.dumps({ "error": "not valid file" }), 500

def get_mendeley_config():
    scheme, netloc, path, query_string, fragment = urlsplit(request.url)
    redirect_url = urlunsplit((scheme, netloc, '/oauth', '', ''))

    return Mendeley(client_id, client_secret, redirect_url)

def get_session_from_cookies():
    return MendeleySession(get_mendeley_config(), session['token'])


def getPdf(session, doc_id):
    """Get pdf from Mendeley document id
    Returns temp pdf object
    """
    doc = session.documents.get(doc_id)

    try:
        doc_url = doc.files.list().items[0].download_url
    except Exception as e:
        print(doc)
        print(doc.files)
        print(doc.files.list())
        raise e
    f = tempfile.NamedTemporaryFile(delete=False)
    f.write(urllib.urlopen(doc_url).read())
    f.close()

    return f

def convertToTxt(pdf):
    """convert PDF (file object) to text, returns text"""
    # text = check_output(["pdftotext", pdf.name, "-"])
    text = check_output(["sh", "parseocr.sh", pdf.name])
    with open(pdf.name+'.met') as f:
        metadata = f.read()
    name = pdf.name
    os.unlink(pdf.name)
    os.unlink(name+'.met')
    return (text, metadata)

def textToEncoded(text):

    with tempfile.NamedTemporaryFile() as temp:
        temp.write(text)
        clean = codecs.open(temp.name,encoding="utf-8").read()

    return clean



if __name__ == '__main__':
    # app.run(host='127.0.0.1', port='5000', debug=False, ssl_context=ssl_context)
    app.run()
