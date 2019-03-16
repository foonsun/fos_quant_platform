from os import makedirs
from os.path import exists as pathexists, dirname, join as pathjoin

def unixsep(path):
    return path.replace('\\', '/')

def unixpathjoin(*args):
    return unixsep(pathjoin(*args))

def norm_fname(fname):
    for illegal_sep in '\\/:*?"<>|':
        fname = fname.replace(illegal_sep, '_')
    return fname

def ensuredir(fdir):
    if not pathexists(fdir):
        makedirs(fdir)

def ensurefiledir(fpath):
    ensuredir(dirname(fpath))

def humanSize(num, suffix='B'):
    for unit in ['','K','M','G','T','P','E','Z']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Y', suffix)
