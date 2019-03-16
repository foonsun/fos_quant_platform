#encoding=utf8

class BaseNetException(Exception):
    def __init__(self, message, *args, **kwargs):
        self.code = kwargs.pop('code', None)
        if self.code is None:
            self.code = -1
        else:
            message = 'code(%s) %s' % (self.code, message)
        super(BaseNetException, self).__init__(message, *args, **kwargs)

class LogicLimitException(BaseNetException):
    def __init__(self, *args, **kwargs):
        super(LogicLimitException, self).__init__(*args, **kwargs)

class LogicIntegrityException(BaseNetException):
    def __init__(self, *args, **kwargs):
        super(LogicIntegrityException, self).__init__(*args, **kwargs)

class LogicAssertException(BaseNetException):
    def __init__(self, *args, **kwargs):
        super(LogicAssertException, self).__init__(*args, **kwargs)

class LogicErrorException(BaseNetException):
    def __init__(self, *args, **kwargs):
        super(LogicErrorException, self).__init__(*args, **kwargs)

def Exc_LogicAssertException(cond, msg='', code=None):
    if not cond:
        raise LogicAssertException(msg, code=code)
