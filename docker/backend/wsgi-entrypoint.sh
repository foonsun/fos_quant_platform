#!/usr/bin/env bash

ls -al /app/blockserver/static/js

until cd /app
do
	echo "waitting for app volume"
done

source env.sh

until cd /app/blockserver
do
    echo "Waiting for server volume..."
done

until ./manage.py migrate
do
    echo "Waiting for mysql ready..."
    sleep 2
done

#./manage.py collectstatic --noinput

gunicorn blockserver.wsgi --bind 0.0.0.0:8000 --workers 4 --threads 4
#./manage.py runserver 0.0.0.0:8000 # --settings=settings.dev_docker
