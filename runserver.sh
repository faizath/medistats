#!/bin/sh

python manage.py migrate
gunicorn medistats.wsgi --bind=0.0.0.0:80