#!/bin/sh

set -e

echo 'Waiting for PostgreSQL...'

while ! nc -z $DB_HOST $DB_PORT; do
    sleep 0.1
done

echo 'PostgreSQL is ready'

echo 'Activating virtual environment...'
ls -a

# Create and activate a virtual environment
python -m venv venv
source /usr/src/app/venv/bin/activate

export PATH="/usr/src/app/venv/bin:$PATH"
pip freeze

# Upgrade pip and install project dependencies using pip
/usr/src/app/venv/bin/pip install --no-cache-dir --upgrade pip \
    && /usr/src/app/venv/bin/pip install --no-cache-dir -r requirements.txt

which python
echo 'Running migrations...'
python manage.py migrate

echo 'Collecting static files...'
python manage.py collectstatic --no-input

echo 'Starting the application...'
exec python manage.py runserver 0.0.0.0:8000
