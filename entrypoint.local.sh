#!/bin/sh

./wait-for-db.sh
python src/manage.py collectstatic --noinput
python src/manage.py migrate --noinput
python -m gunicorn --bind 0.0.0.0:8000 --workers 3 config.wsgi:application