#!/bin/sh

until cd /app
do
    echo "Waiting for server volume..."
done


until python manage.py migrate
do
    echo "Waiting for db to be ready..."
    sleep 2
done


python manage.py collectstatic --noinput

gunicorn clan.wsgi --bind 0.0.0.0:8000 --workers 4 --threads 4
