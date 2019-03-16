import six
import collections
from json import dumps as jdumps

_TITLE_REPLACE = [(u'\u2013', u'-'), (u'\u2026', '...'),
                  (u'\xae', '@'), (u'\u2122', 'TM')]

def toUnicode(text):
    try:
        return text.decode('utf8')
    except Exception as e:
        return text.decode('gb18030')

def toUtf8(text):
    if type(text) is str:
        return text
    elif type(text) is unicode:
        return text.encode('utf8')
    else:
        return str(text)

def bytesToStr(text, likely='utf8'):
    if type(text) is str:
        return text
    if likely == 'utf8':
        guessEncodes = ['utf8', 'gb18030']
    else:
        guessEncodes = ['gb18030', 'utf8']

    for encode in guessEncodes:
        try:
            return text.decode(encode)
        except UnicodeDecodeError as e:
            pass
    return ''

def strToBytes(text, likely='utf8'):
    if type(text) is bytes:
        return text
    return text.encode('utf8')

def normTitle(title):
    if type(title) != unicode:
        title = toUnicode(title)
    for origchar, tgtchar in _TITLE_REPLACE:
        title = title.replace(origchar, tgtchar)
    return title

def hashDigestAlphaIc(chars):
    chars = chars.lower()
    num = 0
    for ch in chars:
        if ch.isdigit():
            num = num * 36 + ord(ch) - ord('0')
        elif ch.isalpha():
            num = num * 36 + (ord(ch) - ord('a') + 10)
    return num

def updateDictRecursive(kwargs0, kwargs1):
    for key, val in kwargs1.items():
        if key not in kwargs0:
            kwargs0[key] = val
            continue
        if type(kwargs0[key]) is dict:
            if type(val) is not dict:
                raise RuntimeError('can not merge key(%s) of %s with %s' % \
                                   (key, jdumps(kwargs0), jdumps(kwargs1)))
            updateDictRecursive(kwargs0[key], val)
        else:
            kwargs0[key] = val
    return kwargs0

def isString(obj):
    return isinstance(obj, six.string_types)

def dumpObject(obj, descdict={}, level=0, objkey='', bytesCharset='utf8'):
    indent = ' '*level*4
    result = []
    otype = type(obj)
    format = ''

    def dumpObj(result, obj, isobject=False):
        if isobject:
            keys = dir(obj)
        else:
            keys = obj.keys()
        for key in keys:
            if isobject:
                val = getattr(obj, key)
                if key.startswith('__'): continue
                if callable(val): continue
            else:
                val = obj[key]
            valtype = type(val)
            # swig types
            if valtype.__name__ == 'SwigPyObject':
                continue
            if key == 'thisown' and valtype is bool:
                continue

            if valtype is int:
                result.append(dumpObject(val, descdict.get(key, {}), level+1, key, bytesCharset))
            elif valtype is float:
                result.append(dumpObject(val, descdict.get(key, {}), level+1, key, bytesCharset))
            elif valtype is bool:
                result.append(dumpObject(val, descdict.get(key, {}), level+1, key, bytesCharset))
            elif isinstance(val, six.string_types):
                result.append(dumpObject(val, descdict.get(key, {}), level+1, key, bytesCharset))
            elif isinstance(val, collections.Iterable):
                result.append(dumpObject(val, descdict.get(key, {}), level+1, key, bytesCharset))
                descitems = descdict.get(key, {})
                if descitems:
                    resultdescList = []
                    if desc is not None:
                        for item in val:
                            desc = descitems.get(item, None)
                            if not desc: continue
                            resultdescList.append(desc)
                    if resultdescList:
                        result.append(','.join(resultdescList))
            else:
                result.append('%s -> \n%s' % (key, dumpObject(val, descdict.get(key, {}), level+1, '', bytesCharset)))

    if otype is int:
        result.append('%s -> int(%s)' % (objkey, obj))
        desc = descdict.get(obj, None)
        if desc is not None: result[-1] += ' %s' % desc
    elif otype is float:
        result.append('%s -> float(%s)' % (objkey, obj))
        desc = descdict.get(obj, None)
        if desc is not None: result[-1] += ' %s' % desc
    elif otype is bool:
        result.append('%s -> bool(%s)' % (objkey, obj))
        desc = descdict.get(obj, None)
        if desc is not None: result[-1] += ' %s' % desc
    elif isinstance(obj, six.string_types):
        result.append('%s -> str(%s)' % (objkey, obj))
        desc = descdict.get(obj, None)
        if desc is not None: result[-1] += ' %s' % desc
    elif otype is bytes:
        if bytesCharset:
            objstr = obj.decode(bytesCharset, 'ignore')
        else:
            objstr = obj
        result.append('%s -> bytes(%s)' % (objkey, objstr))
        desc = descdict.get(obj, None)
        if desc is not None: result[-1] += ' %s' % desc
    elif isinstance(obj, collections.Iterable):
        if hasattr(obj, 'items') and hasattr(obj, 'keys'):
            # dump map
            format = objkey + ' -> object(%s\n'+indent+')'
            dumpObj(result, obj, False)
        else:
            objstrs = []
            for item in obj:
                objstrs.append(dumpObject(item, descdict, level+1, '', bytesCharset))
            result.append('%s -> list[%s\n%s]' % (objkey, ','.join(objstrs), indent))
    else:
        format = objkey + ' -> object(%s\n'+indent+')'
        dumpObj(result, obj, True)

    if format:
        return '\n' + indent + (format % ''.join([indent + item for item in result]))
    else:
        return '\n%s%s' % (indent, ''.join(result))


class ColorPrint:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    INVERT = '\033[7m'
    ENDC = '\033[0m'

    @classmethod
    def header(cls, msg): print(cls.HEADER + msg + cls.ENDC)
    @classmethod
    def blue(cls, msg): print(cls.OKBLUE + msg + cls.ENDC)
    @classmethod
    def green(cls, msg): print(cls.OKGREEN + msg + cls.ENDC)
    @classmethod
    def warning(cls, msg): print(cls.WARNING + msg + cls.ENDC)
    @classmethod
    def fail(cls, msg): print(cls.FAIL + msg + cls.ENDC)
    @classmethod
    def bold(cls, msg): print(cls.BOLD + msg + cls.ENDC)
    @classmethod
    def underline(cls, msg): print(cls.UNDERLINE + msg + cls.ENDC)
    @classmethod
    def blink(cls, msg): print(cls.BLINK + msg + cls.ENDC)
    @classmethod
    def invert(cls, msg): print(cls.INVERT + msg + cls.ENDC)
    
def style(s, style):
    return style + s + '\033[0m'


def green(s):
    return style(s, '\033[92m')


def blue(s):
    return style(s, '\033[94m')


def yellow(s):
    return style(s, '\033[93m')


def red(s):
    return style(s, '\033[91m')


def pink(s):
    return style(s, '\033[95m')


def bold(s):
    return style(s, '\033[1m')


def underline(s):
    return style(s, '\033[4m')

import binascii

class CRC32Calc(object):
    def __init__(self):
        self.crc = 0

    def calcFromFile(self, fpath):
        fstream = open(fpath, 'rb')
        buff = bytearray(4096)
        while True:
            cnt = fstream.readinto(buff)
            if not cnt: break
            data = memoryview(buff)[:cnt]
            self.crc = binascii.crc32(data, self.crc)
        return "%08X" % self.crc

def removePrefix(text, prefix):
    return text[len(prefix):] if text.startswith(prefix) else text

def removePostfix(text, postfix):
    return text[:-len(postfix)] if text.endswith(postfix) else text

class Object(object):
    def __init__(self, **entries):
        self.__dict__.update(entries)
        
def dump(*args):
    print(' '.join([str(arg) for arg in args]))
