DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source $DIR/../env.sh
cd $DIR/..
echo `date`
python -u blockserver/manage.py usdtmonitor
