import threading

class Singleton(object):
    _INSTANCES = {}
    _LOCK = threading.Lock()
    _LOCK_MAP = {}

    @classmethod
    def instance(cls, *args, **kwargs):
        argsnum = len(args)
        kwargsnum = len(kwargs)
        key = '_%s_instance_args%s_kwargs%s' % (cls.__name__, argsnum, kwargsnum)
        if key not in cls._INSTANCES:
            # create one lock to create instance
            with cls._LOCK:
                if key not in cls._LOCK_MAP:
                    cls._LOCK_MAP[key] = threading.Lock()
                instlock = cls._LOCK_MAP[key]
            with instlock:
                if key not in cls._INSTANCES:
                    obj = cls(*args, **kwargs)
                    obj.init()
                    cls._INSTANCES[key] = obj
                    # remove that lock
                    with cls._LOCK:
                        cls._LOCK_MAP.pop(key)
        return cls._INSTANCES[key]

    def __init__(self, *args, **kwargs):
        pass

    def init(self):
        pass

def override(method):
    # TODO:
    return method

def interface(method):
    # TODO:
    return method

class cached_property(object):
    """
    Decorator that converts a method with a single self argument into a
    property cached on the instance.

    Optional ``name`` argument allows you to make cached properties of other
    methods. (e.g.  url = cached_property(get_absolute_url, name='url') )
    """
    def __init__(self, func, name=None):
        self.func = func
        self.__doc__ = getattr(func, '__doc__')
        self.name = name or func.__name__

    def __get__(self, instance, type=None):
        if instance is None:
            return self
        res = instance.__dict__[self.name] = self.func(instance)
        return res

import threading
def threadsafe_function(fn):
    """decorator making sure that the decorated function is thread safe"""
    lock = threading.Lock()
    def new(*args, **kwargs):
        lock.acquire()
        try:
            r = fn(*args, **kwargs)
        except Exception as e:
            raise e
        finally:
            lock.release()
        return r
    return new
