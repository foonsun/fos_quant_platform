#!/usr/bin/env bash

until cd /app
do
	echo "waitting for app volume"
done

source env.sh
export C_FORCE_ROOT="true"

until cd /app/blockserver
do
    echo "Waiting for worker volume..."
done

celery -A blockserver worker --loglevel=info -E
