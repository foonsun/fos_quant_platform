import sys
import importlib
from os import walk
from acom.utils.fileutil import unixpathjoin
from acom.utils.strutil import isString
from os.path import relpath, abspath, exists as pathexists, basename, dirname, join as pathjoin
from acom.command.basecmd import BaseCmd
from inspect import isclass
from json import loads as jloads

class CmdRunner(object):
    def __init__(self, jconf, pkgroot, relpath):
        if isString(jconf):
            self.jconf = jloads(open(jconf).read())
        else: self.jconf = jconf
        self.pkgroot = pkgroot
        self.relpath = relpath
        self.cmdMap = {}
        self.init()

    def init(self):
        basepath = abspath(dirname(self.pkgroot))
        if not pathexists(basepath):
            raise RuntimeError('not exists %s' % basepath)
        sys.path.insert(0, basepath)
        for root, dirs, files in walk(pathjoin(self.pkgroot, self.relpath)):
            relroot = relpath(root, basepath)
            for fname in files:
                if not fname.endswith('.py'): continue
                if not fname.startswith('Cmd'): continue
                cmdname = fname[:-3]
                path = unixpathjoin(relroot, fname)
                if 'cmdname' in self.cmdMap:
                    raise RuntimeError('Duplicate Cmd:\n%s' % '\n'.join(self.cmdMap[cmdname], path))
                self.cmdMap[cmdname] = path

    def getCmdMap(self):
        return self.cmdMap
                
    def genCmdObj(self, cmdname):
        for cmdname0, path in self.cmdMap.items():
            if cmdname0 != cmdname: continue
            cls = self.getCmdCls(path)
            print('== command %s::%s ==' % (cmdname, cls.__name__))
            cmd = cls(cmdname, self.jconf)
            return cmd
        return None

    def getCmdCls(self, path):
        path = path.endswith('.py') and path[:-len('.py')] or path
        imppkg = '.'.join(path.split('/'))
        cmdclsList = []
        modobj = importlib.import_module(imppkg, None)
        for key, val in modobj.__dict__.items():
            if not isclass(val): continue
            if not issubclass(val, BaseCmd): continue
            if val is BaseCmd: continue
            if val.__name__ != 'Command': continue
            cmdclsList.append(val)
            break
        if len(cmdclsList) != 1:
            raise RuntimeError('Cmd Class not single %s\n%s' % (','.join(cmdclsList), path))
        return cmdclsList[0]

    def main(self, cmdname, argv):
        cmdobj = self.genCmdObj(cmdname)
        if not cmdobj:
            self.printHelp()
            return -1
        else:
            cmdobj.setup()
            return self.runCmdObj(cmdobj, argv, None, None)

    def runCmdObj(self, cmdobj, argv, stdout=None, stderr=None):
        if stdout:
            cmdobj.appendStdout(stdout)
        if stderr:
            cmdobj.appendStderr(stderr)
        cmdobj._parseArgv(argv)
        cmdobj.init()
        return cmdobj.work()

    def runCmdObjArgs(self, cmdobj, stdout=None, stderr=None, **kwargs):
        argv = ''
        for key, val in kwargs.items():
            argv.append('--%s=%s' % (key, val))
        return self.runCmdObj(cmdobj, argv, stdout, stderr)

    def printHelp(self):
        print('Help:')
        maxlen = 0
        for cmdname, path in self.cmdMap.items():
            cmdlen = len(cmdname)
            if cmdlen > maxlen:
                maxlen = cmdlen
        outfmt = '%'+str(maxlen)+'s\t%s'
        for cmdname, path in self.cmdMap.items():
            print(outfmt % (cmdname, path))
