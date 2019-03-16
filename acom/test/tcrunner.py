import sys
import importlib
from os import walk
from acom.utils.fileutil import unixpathjoin
from os.path import relpath, abspath, exists as pathexists, dirname, join as pathjoin
from acom.test.tcbase import TcBase
from inspect import isclass

class TcRunner(object):
    def __init__(self, pkgroot, relpath, namematch):
        self.pkgroot = pkgroot
        self.relpath = relpath
        self.namematch = namematch
        slist = self.namematch.split('.')
        if len(slist) == 1:
            self.filematch = slist[0]
            self.funcmatch = ''
        elif len(slist) > 1:
            self.filematch = slist[0]
            self.funcmatch = slist[1]

    def main(self):
        basepath = abspath(dirname(self.pkgroot))
        if not pathexists(basepath):
            raise RuntimeError('not exists %s' % basepath)
        sys.path.insert(0, basepath)
        validlist = []
        for root, dirs, files in walk(pathjoin(self.pkgroot, self.relpath)):
            relroot = relpath(root, basepath)
            for fname in files:
                if not fname.endswith('.py'): continue
                if not fname.startswith(self.filematch): continue
                validlist.append(unixpathjoin(relroot, fname))
    
        for path in validlist:
            path = path.endswith('.py') and path[:-len('.py')] or path
            imppkg = '.'.join(path.split('/'))
            modobj = importlib.import_module(imppkg, None)
            for key, val in modobj.__dict__.items():
                if not isclass(val): continue
                if not issubclass(val, TcBase): continue
                if val is TcBase: continue
                print('== testcase (%s) ==' % key)
                val().work(self.funcmatch)
