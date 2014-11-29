import os
from urlparse import urlsplit, urlunsplit

from flask import Flask, redirect, render_template, request, session
from mendeley import Mendeley
from mendeley.session import MendeleySession
from werkzeug.contrib.fixers import ProxyFix


client_id = os.environ['MENDELEY_CLIENT_ID']
client_secret = os.environ['MENDELEY_CLIENT_SECRET']

app = Flask(__name__)
app.debug = True
app.secret_key = client_secret
app.wsgi_app = ProxyFix(app.wsgi_app)


@app.route('/')
def login():
    if 'token' in session:
        return redirect('/home')

    mendeley = get_mendeley_config()
    auth = mendeley.start_authorization_code_flow()

    session['state'] = auth.state

    return render_template('login.html', login_url=(auth.get_login_url()))


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
    if 'token' not in session:
        return redirect('/')

    mendeley_session = get_session_from_cookies()

    name = mendeley_session.profiles.me.display_name

    return render_template('home.html', name=name)


@app.route('/logout')
def logout():
    session.pop('token', None)
    return redirect('/')


def get_mendeley_config():
    scheme, netloc, path, query_string, fragment = urlsplit(request.url)
    redirect_url = urlunsplit((scheme, netloc, '/oauth', '', ''))

    return Mendeley(client_id, client_secret, redirect_url)


def get_session_from_cookies():
    return MendeleySession(get_mendeley_config(), session['token'])


if __name__ == '__main__':
    app.run()
