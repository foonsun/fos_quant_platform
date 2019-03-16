from argparse import ArgumentParser
from acom.utils.logger import SimpleLoggerMixin
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

class BaseCmd(SimpleLoggerMixin):
    def __init__(self, prog, jconf, *args, **kwargs):
        self.prog = prog
        self.jconf = jconf
        self.parser = ArgumentParser(prog=prog)
        self.opts = None
        self.ostream = None
        SimpleLoggerMixin.__init__(self)
        self._initStream()

    def _initStream(self):
        self.ostream = StringIO()
        self.appendStdout(self.ostream)
        self.appendStderr(self.ostream)

    def getOutPrint(self):
        if self.ostream:
            return self.ostream.getvalue()
        else: return ''

    # for options init
    def setup(self):
        pass

    # for variable init
    def init(self):
        pass

    def work(self):
        raise NotImplementedError

    def _parseArgv(self, argv):
        self.opts = self.parser.parse_args(argv)

    # nargs in ('*', '+', '?')
    def addListOpt(self, optstr, default=[], help_='', nargs='*', required=False):
        kwargs = dict(default=default, nargs=nargs,
                      required=required, help=help_)
        if nargs == '?':
            kwargs['const'] = default
        self.parser.add_argument(*optstr.split(), **kwargs)

    def addBoolOpt(self, optstr, default=False, help_='', required=False):
        if not default: action = 'store_true'
        else: action = 'store_false'
        self.parser.add_argument(*optstr.split(), action=action, required=required, help=help_)

    def addStrOpt(self, optstr, default='', help_='', required=False):
        self.parser.add_argument(*optstr.split(), type=str, default=default,
                                 required=required, help=help_)

    def addIntOpt(self, optstr, default=0, help_='', required=False):
        self.parser.add_argument(*optstr.split(), type=int, default=default,
                                 required=required, help=help_)

    def addFloatOpt(self, optstr, default=0.0, help_='', required=False):
        self.parser.add_argument(*optstr.split(), type=float, default=default,
                                 required=required, help=help_)

    def addChoiceOpt(self, optstr, choices, default=None, help_='', required=False):
        if not choices: raise RuntimeError('choices can not be null')
        if default is None: default=choices[0]
        self.parser.add_argument(*optstr.split(), type=type(choices[0]),
                                 choices=choices, required=required, help=help_,
                                 default=default)

    def dumpOpts(self):
        return ','.join([ '%s(%s)' % (key, val) for key, val in \
                            self.opts.__dict__.items() ])

