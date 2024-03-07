#!/bin/sh

set -e

echo 'Waiting for PostgreSQL...'

while ! nc -z $DB_HOSTNAME $DB_PORT; do
    sleep 0.1
done

echo 'PostgreSQL is ready'

echo 'Running migrations...'
python manage.py migrate

echo 'Collecting static files...'
python manage.py collectstatic --no-input

echo 'Starting the application...'
exec "$@"

trap 'echo "Stopping..."; exit 0' SIGTERM
