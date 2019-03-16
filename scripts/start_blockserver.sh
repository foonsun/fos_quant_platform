#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source $DIR/../env.sh
CMD1="daphne -b 0.0.0.0 -p 8001 blockserver.asgi:application"
$CMD1
disown -ah
