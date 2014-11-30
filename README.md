EasySkim
========

##Analyse and summarise your academic papers

Synchronise with your Mendeley library using their API or upload your own PDFs. EasySkim then processes the text from the pdf and uses natural language processing algorithms to produce brief summaries of the key sections of the paper. 

Originally developed at [oxHack 2014](http://oxhack.co.uk/)

### Progress
At present, works locally on Mac and Linux machines, assuming requirements are satsified. This does require a Mendeley client ID and secret.

Deployment to website is pending OAuth2 and SSL fixes.

Our Website (in progress): [easyskim.co.uk](http://easyskim.co.uk) 
<br> 
Twitter: [@easyskim](https://twitter.com/easyskim)
<br>
Email us: [admin@easyskim.co.uk](mailto:admin@easyskim.co.uk)

<i>Apache Licence Version 2.0</i>


### Installation
Installation requires Python 2.7+ and pip. Mendeley Client ID and Secret can be obtained from [Mendeley Dev](http://dev.mendeley.com/) and must be exported as variables before launching the app.


```
git clone https://github.com/rebeccamorgan/easyskim.git
cd easyskim

pip install -r requirements.txt

export MENDELEY_CLIENT_ID= < >
export MENDELEY_CLIENT_SECRET= < >

```

### Use

```
python app.py
```

Visit the localhost address e.g. ```localhost:5000``` in your browser to use the app.
