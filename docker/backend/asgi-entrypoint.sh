#!/usr/bin/env bash

until cd /app
do
	echo "waitting for app volume"
done

source env.sh

until cd /app/fieldkeys
do
	rm -f 1
	rm -f meta
	keyczart create --location=../fieldkeys --purpose=crypt
	keyczart addkey --location=../fieldkeys --status=primary --size=256
done

until cd /app/blockserver
do
    echo "Waiting for server volume..."
done

until echo y | ./manage.py makemigrations
do
    echo "Waiting for mysql ready..."
    sleep 3
done

until echo y | ./manage.py makemigrations blockuser sanjiao duiqiao
do
    echo "Waiting for mysql ready..."
    sleep 3
done

./manage.py migrate
./manage.py collectstatic --noinput

daphne blockserver.asgi:application --bind 0.0.0.0 --port 8000
