#!/usr/bin/env bash

until cd /app
do
	echo "waitting for app volume"
done

source env.sh


until cd /app/blockserver
do
    echo "Waiting for server volume..."
done

until echo y | ./manage.py makemigrations
do
    echo "Waiting for mysql ready..."
    sleep 3
done

until echo y | ./manage.py makemigrations sanjiao duiqiao
do
    echo "Waiting for mysql ready..."
    sleep 3
done

./manage.py migrate
./manage.py collectstatic --noinput

mkdir -p logs/pyexchanges
mkdir -p logs/fcoin
mkdir fieldkeys
keyczart create --location=fieldkeys --purpose=crypt
keyczart addkey --location=fieldkeys --status=primary --size=256

daphne blockserver.asgi:application --bind 0.0.0.0 --port 8000