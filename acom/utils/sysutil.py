import sys
import platform
from time import time
from datetime import timedelta
from urllib.request import urlopen

if sys.platform == 'win32':
    cmdencode = 'gbk'
else:
    cmdencode = 'utf8'

def isWindowsSystem():
    return 'Windows' in platform.system()

def isLinuxSystem():
    return 'Linux' in platform.system()

def isMacSystem():
    return 'Darwin' in platform.system()

def dateRange(start, end, filterFunc=None, reverse=False):
    delta = end - start
    if not reverse:
        for idx in range(delta.days+1):
            dtobj = (start + timedelta(days=idx))
            if filterFunc and not filterFunc(dtobj):
                continue
            yield dtobj
    else:
        for idx in range(delta.days+1):
            dtobj = (end - timedelta(days=idx))
            if filterFunc and not filterFunc(dtobj):
                continue
            yield dtobj

def CheckUrlAvailable(url=None, timeout=5):
    try:
        if url == None:
            return False
        ret = urlopen(url, timeout=timeout)
        if ret.code == 200:
            return True
        else:
            return False
    except:
            return False

