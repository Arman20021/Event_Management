#!/usr/bin/env bash
# exit on error
set -o errexit

python manage.py migrate
python manage.py loaddata local_data.json
python manage.py runserver 0.0.0.0:80