
# #wikidev
Wikipedia-based service written in Django/Python.
This is a stripped down/mockup version of the #wiki application found on the ONEm platform.
It uses the ONEm developer framework.


## Direct usage
Head to https://poc.onem.zone/ and send #wikidev.

## Installation

Clone the repo:
```
git clone https://github.com/bogdanta/wikidev.git
```

Go to the repo's root folder:
```
cd wikidev
```

Install the requirements(in a virtual environment):
```
pip install -r requirements.txt
```

Migrate Django's base models and start the local server
```
python manage.py migrate
python manage.py runserver
```

Install [ngrok](https://ngrok.com/download) and start a tunnel:
```
ngrok http 8000
```
Register the app on the [ONEm developer portal](https://developer-portal-poc.onem.zone/))(under a different name eg. #wikinew):
Set the callback URL to the forwarding address obtained from ngrok's output, go to the [sandbox](https://poc.onem.zone/) and send #wikinew.


### Deploy to Heroku
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)
