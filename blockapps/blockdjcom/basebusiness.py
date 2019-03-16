#encoding=utf8
import threading
from django.utils.functional import cached_property
from django.core.exceptions import PermissionDenied
from blockcomm.net.exceptions import Exc_LogicAssertException,\
    LogicErrorException, LogicAssertException
from blockcomm.context import BaseContext
from djcom.utils import get_client_ip, get_server_ip

'''
Source Singleton 用于定义不同产品来源(source)逻辑实现单例，逻辑主要分两类实现：
1. 对于不同的产品来源(source)具有统一的逻辑处理层;
2. 对于不同的产品来源(source)具有不同的处理逻辑;

* 对于第一种情况，直接作为单例使用;
* 对于第二种情况，面向接口编程，对具体的实现以继承多态的形式封装;
* 第二种情况使用方式
```
BaseClass(SSingleton):
    def init(self):
        pass
SSingleton.register(SOURCE_ID)
class Subclass(BaseClass):
    pass
```

* 对于每个业务接口通常第一个参数为 context，其中包含了业务公共的参数
    * apikey
    * apisecret
'''
class SSingleton(object):
    _INSTANCES = {}
    _LOCK = threading.Lock()
    _LOCK_MAP = {}
    _SOURCE_CLS_MAP = {}
    @classmethod
    def instance(cls, source, *args, **kwargs):
        Exc_LogicAssertException(source in (SSingleton.QQREADER, SSingleton.QIDIAN))
        argsnum = len(args)
        kwargsnum = len(kwargs)
        key = '_%s_%s_instance_args%s_kwargs%s' % (cls.__name__, source, argsnum, kwargsnum)
        if key not in cls._INSTANCES:
            # create one lock to create instance
            with cls._LOCK:
                if key not in cls._LOCK_MAP:
                    cls._LOCK_MAP[key] = threading.Lock()
                instlock = cls._LOCK_MAP[key]
            with instlock:
                if key not in cls._INSTANCES:
                    clskey = '_%s_%s' % (cls.__name__, source)
                    actualCls = cls._SOURCE_CLS_MAP.get(clskey, cls)
                    obj = actualCls(source, *args, **kwargs)
                    obj.init()
                    cls._INSTANCES[key] = obj
                    # remove that lock
                    with cls._LOCK:
                        cls._LOCK_MAP.pop(key)
        return cls._INSTANCES[key]

    @classmethod
    def register(cls, source, rootCls=None):
        def wrap(subcls):
            rootCls0 = rootCls
            if rootCls0 is None:
                rootCls0 = subcls.__base__
            clskey = '_%s_%s' % (rootCls0.__name__, source)
            rootCls0._SOURCE_CLS_MAP[clskey] = subcls
            return subcls
        return wrap

    def __init__(self, source, *args, **kwargs):
        self.source = source

    def init(self):
        pass

class Context(BaseContext):
    def __init__(self, *args, **kwargs):
        super(Context, self).__init__(*args, **kwargs)
        self.nocache = 0

    def KeyVerifyRequired(self):
        if not self.apikey:
            raise PermissionDenied('apikey is required')
        if not self.apisecret:
            raise PermissionDenied('secret is required')
        else:
            pass

    def fillRequest(self, request):
        self.clientip = get_client_ip(request)
        self.serverip = get_server_ip(request)

    @classmethod
    def ServerContext(ctx, source):
        ctx = Context()
        return ctx