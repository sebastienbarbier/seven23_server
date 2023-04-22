#!/bin/sh

if [ -z "$SECRET_KEY" ]; then
  echo "WARNING: No SECRET_KEY set. Please generate one and export it as SECRET_KEY env variable."
  export SECRET_KEY=$(tr -dc 'a-z0-9!@#$%^&*(-_=+)' < /dev/urandom | head -c50)
  echo "Temporary one created. This will be lost on restart and deprecate all open session forcing user to reload."
fi

export COMPRESS_OFFLINE=True

python manage.py compilescss
python manage.py collectstatic --noinput
python manage.py migrate
python manage.py loaddata seven23/models/currency/fixtures/initial_data.json

gunicorn seven23.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 3