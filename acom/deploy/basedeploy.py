#encoding=utf8
from os import system as ossystem
from os.path import exists as pathexists

class BaseDeploy(object):
    def runcmd(self, cmd, check=True):
        print(cmd)
        ret = ossystem(cmd)
        if check and ret != 0:
            raise RuntimeError('execute failed cmd: %s' % cmd)
        return ret
    
    def rm(self, target, check=False):
        cmd = 'rm -rf %s' % target
        return self.runcmd(cmd, check)

    def cp(self, source, target, check=True):
        cmd = 'cp -a %s %s' % (source, target)
        return self.runcmd(cmd, check)
        
    def chmod(self, mode, target, check=True):
        cmd = 'chmod -R %s %s' % (mode, target)
        return self.runcmd(cmd, check)

    def install(self, source, target, mode, check=True):
        result = True
        result &= self.cp(source, target, check)
        result &= self.chmod(mode, target, check)
        return result
    
    def strip(self, target, check=True):
        cmd = 'strip %s' % target
        return self.runcmd(cmd, check)
    
    def cleanPyc(self, tgtdir, check=True):
        return self.runcmd(r'cd %s && find -name *.pyc -o -name *.pyd -o -name *.pyo | xargs rm --' % tgtdir, check)

    def checkGitDir(self, basedir, gitname):
        if not pathexists('%s/.git' % basedir):
            raise RuntimeError('basedir is not a git dir: %s' % basedir)
        with open('%s/.git/config' % basedir) as fp:
            content = fp.read()
        if gitname not in content:
            raise RuntimeError('basedir is not %s git: %s' % (gitname, basedir))
        return basedir

    def gitPull(self, gitdir, check=True):
        cmd = 'cd %s; git pull' % gitdir
        return self.runcmd(cmd, check)

    def gitPush(self, gitdir, check=True):
        cmd = 'cd %s; git push' % gitdir
        return self.runcmd(cmd, check)

    def gitChangeBranch(self, gitdir, gitbranch, check=True):
        cmd = 'cd %s; git checkout %s' % (gitdir, gitbranch)
        return self.runcmd(cmd, check)
        
    def gitAdd(self, gitdir, target, check=True):
        cmd = 'cd %s; git add %s' % (gitdir, target)
        return self.runcmd(cmd, check)

    def gitCommit(self, gitdir, comment, check=True):
        cmd = 'cd %s; git commit -m "%s"' % (gitdir, comment)
        return self.runcmd(cmd, check)

    def gitAddTag(self, gitdir, tagname, comment=None, check=True):
        result = True
        if comment is None:
            comment = 'add tag %s' % tagname
        cmd = 'cd %s; git tag -a %s -m "%s"' % (gitdir, tagname, comment)
        result &= self.runcmd(cmd, check)
        cmd = 'cd %s; git push origin %s' % (gitdir, tagname)
        result &= self.runcmd(cmd, check)
