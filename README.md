
# #wikidev
Wikipedia-based service written in Django/Python.
This is a stripped down/mockup version of the #wiki application found on the ONEm platform.
It uses the ONEm developer framework.


## Direct usage of the app
Head to https://poc.onem.zone/ and send #wikidev.
Note: the app currently runs on my local machine(aka it is not deployed) so if a "Something is wrong with #WIKIDEV. Please try again." message is received it means my local Django server needs to be started.



## Instalation

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
python manage.py runserver 0.0.0.0:8000
```

Register the app on the [ONEm developer portal](https://developer-portal-poc.onem.zone/))(under a different name eg. #wikinew):
Set the callback URL to 0.0.0.0:8000, go to the [sandbox](https://poc.onem.zone/) and send #wikinew.



