#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source $DIR/../env.sh
ps aux | grep "daphne" | grep -v -e "grep" | awk '{print $2}' | xargs kill -9
