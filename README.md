EasySkim
========

##Analyse and summarise your academic papers
### Version 0.1

Synchronise with your Mendeley library using their API or upload your own PDFs. EasySkim then processes the text from the pdf and uses natural language processing algorithms to produce brief summaries of the key sections of the paper. 

Originally developed at [oxHack 2014](http://oxhack.co.uk/)

### Progress
At present, works locally on Mac and Linux machines, assuming requirements are satsified. This does require a Mendeley client ID and secret.

Deployment to website is pending OAuth2 and SSL fixes.

Our Website (in progress): [easyskim.co.uk](https://easyskim.co.uk) 
<br>
YouTube [Demonstration](https://www.youtube.com/watch?v=S7qVVjXWuCk&feature=youtu.be)
<br> 
Twitter: [@easyskim](https://twitter.com/easyskim)
<br>
Email us: [admin@easyskim.co.uk](mailto:admin@easyskim.co.uk)

<i>Apache Licence Version 2.0</i>


### Installation
Installation requires Python 2.7+, pip, pdftotext (within poppler) and exiftool (python package dependencies are installed later by pip). Mendeley Client ID and Secret can be obtained from [Mendeley Dev](http://dev.mendeley.com/) and must be exported as variables before launching the app, where < > are replaced by the values you receive from the website. 

For the "Redirect URL", use a local host such as ```http://localhost:5000/oauth``` and then click "Generate Secret". The name and description is anything of your choice.


```
git clone https://github.com/rebeccamorgan/easyskim.git
cd easyskim

pip install -r requirements.txt

export MENDELEY_CLIENT_ID=< >
export MENDELEY_CLIENT_SECRET=< >
```

For example:

```
export MENDELEY_CLIENT_ID=1181
export MENDELEY_CLIENT_SECRET=kUSg3oEFhb58TAez
```

Within the python interpreter, install nltk libraries as described [here](http://www.nltk.org/data.html) which launches the GUI installer.

```
import nltk
nltk.download()
```


### Temporary Local Use

```
python app.py
```
The output of this will be something like:

```
 * Running on http://127.0.0.1:5000/
 * Restarting with reloader
 ```
 
Visit the localhost address, substituting this phrase in for e.g. ```127.0.0.1``` in this case. For this example, visit ```localhost:5000``` in your browser to use the app with Mendeley.
