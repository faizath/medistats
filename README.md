# Medistats
Simple Hosted Medical Data Logging Tool

## Installation
Deployment through caprover
```
git clone https://github.com/faizath/medistats.git
cd medistats
caprover deploy -b master
```

Manual deployment
```
git clone https://github.com/faizath/medistats.git
cd medistats
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```