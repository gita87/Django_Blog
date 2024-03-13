#!/bin/sh

set -e

echo 'Waiting for PostgreSQL...'

while ! nc -z $DB_HOST $DB_PORT; do
    sleep 0.1
done

echo 'PostgreSQL is ready'

echo 'Running migrations...'
/app/venv/bin/python /app/manage.py migrate

echo 'Collecting static files...'
/app/venv/bin/python /app/manage.py collectstatic --no-input

echo 'Starting the application...'
exec /app/venv/bin/gunicorn --bind 0.0.0.0:8000 blog_project.wsgi:application