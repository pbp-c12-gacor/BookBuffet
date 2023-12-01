#!/usr/bin/env bash
# exit when any command fails
set -o errexit

# build the project
pip install -r requirements.txt

# collect static files
python manage.py collectstatic --no-input

# migrate db, so we have the latest db schema
python manage.py migrate