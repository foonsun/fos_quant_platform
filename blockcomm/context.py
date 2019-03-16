#encoding=utf8
from blockcomm.net.exceptions import LogicErrorException,\
    Exc_LogicAssertException, LogicAssertException
from acom.utils.designutil import cached_property

class BaseContext(object):
    def __init__(self, apikey, apisecret):
        self.apikey = str(apikey)
        self.apisecret = str(apisecret)
        self.clientip = '0.0.0.0'
        self.serverip = '0.0.0.0'

    def __str__(self, *args, **kwargs):
        return 'apikeys(%s) apisecret(%s) token(%s) source(%s) serial(%s)' % \
            (self.apikey, self.apisecret)

    def clone(self):
        return self.__class__(self.usertype, self.userid, self.token, self.source,
                self.serial, self.nickname)

    def checkValid(self, withExcept):
        msg = ''
        if type(self.apikey) is not str:
            msg = 'apikey(%s) not valid' % self.apikey
        if type(self.apisecret) is not str:
            msg = 'apisecret(%s) not valid' % self.apisecret
        if msg and withExcept:
            raise LogicAssertException(msg)

    @cached_property
    def uuser(self):
        pass