#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py flush --no-input
python manage.py collectstatic --no-input
python manage.py migrate
# Use verbosity 3 so we can see exactly what happens in the logs
python manage.py loaddata local_data.json --verbosity 3