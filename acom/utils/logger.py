import sys
from os import makedirs
from datetime import datetime
from os.path import split as pathsplit, exists as pathexists
from json import dumps as jdumps, loads as jloads

class Logger(object):
    def __init__(self, fpath):
        self.fpath = fpath
        dir0, fname0 = pathsplit(fpath)
        if dir0 and not pathexists(dir0):
            makedirs(dir0)
        self.fp = open(self.fpath, 'a')

    def gettime(self):
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def dolog(self, prefix, msg):
        msg = '[%s][%s] %s' % (prefix, self.gettime(), msg)
        self.fp.write(msg)
        self.fp.write('\n')
        self.fp.flush()
        sys.stdout.write(msg)
        sys.stdout.write('\n')
        sys.stdout.flush()
        
    def rawlog(self, msg):
        self.fp.write(msg)
        sys.stdout.write(msg)
        sys.stdout.flush()
        
    def i(self, msg): self.dolog('I', msg)
    def d(self, msg): self.dolog('D', msg)
    def w(self, msg): self.dolog('W', msg)
    def e(self, msg): self.dolog('E', msg)
    
LOG = Logger('logger.log')

class JsonConfig(object):
    def __init__(self, fpath):
        self.fpath = fpath
        self.conf = None
        self._load()

    def _load(self):
        if not pathexists(self.fpath):
            self.conf = {}
            return
        with open(self.fpath, 'rt') as fp:
            self.conf = jloads(fp.read())

    def _save(self):
        with open(self.fpath, 'wt') as fp:
            fp.write(jdumps(self.conf))

    def get(self, key, defval=None):
        return self.conf.get(key, defval)

    def set(self, key, val):
        if val == self.get(key): return
        self.conf[key] = val
        self._save()
        
class SimpleLoggerMixin(object):
    def __init__(self, stdouts=[sys.stdout,], stderrs=[sys.stderr,]):
        self.stdouts = stdouts
        self.stderrs = stderrs

    def appendStdout(self, stdout):
        self.stdouts.append(stdout)

    def appendStderr(self, stderr):
        self.stderrs.append(stderr)

    def _message(self, prefix, msg):
        return '%s%s %s\n' % (prefix, datetime.now().strftime('[%Y%m%d %H:%M:%S]'), msg)

    def info(self, msg):
        self.rawout(self._message('[INFO] ', msg))

    def warn(self, msg):
        self.rawerr(self._message('[WARN] ', msg))

    def error(self, msg):
        self.rawerr(self._message('[ERROR]', msg))

    def debug(self, msg):
        self.rawerr(self._message('[ERROR]', msg))

    def rawout(self, msg):
        for stdout in self.stdouts:
            stdout.write(msg)
            stdout.flush()

    def rawerr(self, msg):
        for stderr in self.stderrs:
            stderr.write(msg)
            stderr.flush()

    def printout(self, msg):
        self.rawout('%s\n' % msg)

    def printerr(self, msg):
        self.rawerr('%s\n' % msg)

class ConsoleLoggerMixin(object):
    def _message(self, prefix, msg):
        return '%s%s %s\n' % (prefix, datetime.now().strftime('[%Y%m%d %H:%M:%S]'), msg)

    def info(self, msg):
        self.rawout(self._message('[INFO] ', msg))

    def warn(self, msg):
        self.rawerr(self._message('[WARN] ', msg))

    def error(self, msg):
        self.rawerr(self._message('[ERROR]', msg))

    def debug(self, msg):
        self.rawerr(self._message('[ERROR]', msg))

    def rawout(self, msg):
        sys.stdout.write(msg)
        sys.stdout.flush()

    def rawerr(self, msg):
        sys.stderr.write(msg)
        sys.stderr.flush()

    def printout(self, msg):
        self.rawout('%s\n' % msg)

    def printerr(self, msg):
        self.rawerr('%s\n' % msg)
