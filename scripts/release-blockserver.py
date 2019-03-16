#!/usr/bin/env python
import os, sys
from os import makedirs
from os.path import exists as pathexists, dirname, join as pathjoin
from shutil import rmtree
from datetime import datetime
from acom.deploy.basedeploy import BaseDeploy

class Deploy(BaseDeploy):
    def __init__(self, deployType, basedir):
        self.deployType = deployType
        self.basedir = basedir
        self.datestr = datetime.now().strftime('%Y%m%d_%H%M%S')
        if deployType == 'git':
            self.gitdir = self.checkGitDir(basedir, 'blockserver_deploy.git')
            self.gitbranch = 'master'

    def copyFiles(self, tgtdir0):
        for fileOrDir in ('3rdapps', 'blockapps',
                'blockserver', 'env.sh', 'acom', 'blockcomm',
                'fieldkeys',
                ('scripts/start_blockserver.sh', '775'),
                ('scripts/stop_blockserver.sh', '775'),
                ('conf/loggings.json', '644'),
                ('conf/mongo-online.json', '644'),
                ('conf/mongo-pre.json', '644'),
                ('conf/mongo-uat.json', '644'),
                ('conf/mongo-localhost.json', '644'),
                ('conf/caches-online.json', '644'),
                ('conf/caches-pre.json', '644'),
                ('conf/caches-uat.json', '644'),
                ('conf/caches-localhost.json', '644'),
                ('conf/siteconfig-online.json', '644'),
                ('conf/siteconfig-pre.json', '644'),
                ('conf/siteconfig-uat.json', '644'),
                ('conf/siteconfig-localhost.json', '644'),
                ):
            if type(fileOrDir) in (tuple, list):
                fileOrDir, permission = fileOrDir
            else:
                permission = None
            if not pathexists(fileOrDir):
                raise RuntimeError('can not find %s' % fileOrDir)
            tgt = '%s/%s' % (tgtdir0, fileOrDir)
            tgtdir = dirname(tgt)
            if not pathexists(tgtdir):
                makedirs(tgtdir)
            self.cp(fileOrDir, tgt)
            if permission:
                self.chmod(permission, tgt)

        # clean pyc pyo pyd pyo
        self.cleanPyc(tgtdir0)

    # --------------------- git ---------------------
    def deleteGitFiles(self):
        self.rm('%s/*' % self.gitdir)

    def addGitFiles(self):
        self.runcmd('cd %s; git ls-files --deleted | xargs -I {}  git rm {}' % self.gitdir)
        self.gitAdd(self.gitdir, '*')
        self.gitCommit(self.gitdir, 'update release %s' % self.datestr)
        self.gitPush(self.gitdir)

    def updateGitTag(self, ver):
        self.gitAddTag(self.gitdir, ver)

    def addGitVerfile(self, ver):
        with open(pathjoin(self.gitdir, '%s.txt' % ver), 'wt') as fp:
            fp.write(ver)

    def work(self):
        ver = 'ver-%s' % self.datestr
        if self.deployType == 'git':
            self.gitChangeBranch(self.gitdir, self.gitbranch)
            self.deleteGitFiles()
            self.copyFiles(self.gitdir)
            self.addGitVerfile(ver)
            self.addGitFiles()
            self.updateGitTag(ver)
        elif self.deployType == 'copy':
            self.copyFiles(self.basedir)
        else:
            raise RuntimeError('unknown deploy type %s' % self.deployType)

from os.path import dirname, abspath
TOPDIR = abspath(dirname(dirname(__file__)))
if __name__ == '__main__':
    deployType = 'git'
    basedir = '%s/blockserver_deploy' % dirname(TOPDIR)
    args = sys.argv[1:3]
    def printUsage():
        print('%s <deployType> [basedir]' % sys.argv[0])

    if len(args) == 2:
        deployType, basedir = args
    elif len(args) == 1:
        if args[0] in ('help', '-h', '--help'):
            printUsage()
            sys.exit(-1)
        deployType = args[0]
    elif len(args) == 0:
        pass
    else:
        printUsage()
        sys.exit(-1)
    print('deployType %s' % deployType)
    print('basedir %s' % basedir)
    Deploy(deployType, basedir).work()

