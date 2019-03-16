#encoding=utf8

class BlockException(Exception):
    def __init__(self, message, *args, **kwargs):
        self.code = kwargs.pop('code', None)
        if self.code is None:
            self.code = -1
        super(BlockException, self).__init__(message, *args, **kwargs)

class LogicLimitException(BlockException):
    def __init__(self, *args, **kwargs):
        super(LogicLimitException, self).__init__(*args, **kwargs)

class LogicIntegrityException(BlockException):
    def __init__(self, *args, **kwargs):
        super(LogicIntegrityException, self).__init__(*args, **kwargs)

class LogicAssertException(BlockException):
    def __init__(self, *args, **kwargs):
        super(LogicAssertException, self).__init__(*args, **kwargs)

class LogicErrorException(BlockException):
    def __init__(self, *args, **kwargs):
        super(LogicErrorException, self).__init__(*args, **kwargs)

def Exc_LogicAssertException(cond, msg='', code=None):
    if not cond:
        raise LogicAssertException(msg, code=code)
