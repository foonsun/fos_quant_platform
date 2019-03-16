from blockdjcom.basebusiness import Context, SSingleton
class TcConfig(object):
    API_KEY = ''
    API_SECRET = ''
    @classmethod
    def CreateContext(cls, apikey=TcConfig.API_KEY, apisecret=TcConfig.API_SECRET): # TODO use command or file config
        ctx = Context(apikey, apisecret)
        return ctx
