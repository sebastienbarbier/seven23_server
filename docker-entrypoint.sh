#!/bin/bash

python manage.py collectstatic --noinput
python manage.py migrate
python manage.py loaddata seven23/models/currency/fixtures/initial_data.json

# FIXME serve static assets from dedicated web server
python manage.py runserver 0.0.0.0:${PORT:-8000} --insecure
