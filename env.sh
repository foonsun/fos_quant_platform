TOPDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export PYTHONPATH=.:$TOPDIR:$TOPDIR/blockapps:$TOPDIR/3rdapps:$TOPDIR/py3rd/scons-2.5.1:$TOPDIR/blockmanage:$TOPDIR/blockserver
export PATH=$TOPDIR/tools:$TOPDIR/bin:$PATH
source ~/pyenv/bin/activate

export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8
