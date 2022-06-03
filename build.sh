#!/usr/bin/env bash
# exit on error
set -o errexit

pip install pip --upgrade
pip install -r requirements.txt
pip install gunicorn

ls /var/data
touch /var/data/db.sqlite3

python manage.py collectstatic --no-input
python manage.py makemigrations
python manage.py migrate
