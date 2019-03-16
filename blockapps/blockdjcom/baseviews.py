#encoding=utf8
import traceback
from hashlib import md5
from time import time
from json import loads as jloads, dumps as jdumps
from json.decoder import JSONDecodeError
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.views.generic.base import View
from django.conf import settings
from acom.utils.strutil import ColorPrint
from blockdjcom.decorators import block_json, monit_time
from blockdjcom.basebusiness import Context, SSingleton
from blockcomm.net.exceptions import LogicErrorException
from djcom.utils import get_client_ip, get_server_ip

RUNSERVER_MODE = settings.RUNSERVER_MODE

class JsonView(View):
    @method_decorator(block_json)
    @method_decorator(require_POST)
    def dispatch(self, request, *args, **kwargs):
        self.__tmstart = time()
        ctx = self._parse_ctx(request)
        resultInfo = {}
        try:
            successCnt = 0
            cacheStatus = 'unknown'
            resultInfo = self._dispatch(ctx, request, *args, **kwargs)
            successCnt += 1
            if resultInfo['cache']:
                cacheStatus = 'cache'
            else:
                cacheStatus = 'nocache'
            return resultInfo['result']
        finally:
            clientIp = ctx.clientip
            requestPath = request.path_info
            requestType = 'jsonapi'

            timeConsume = self._deltaTime()
            # 目前没有异步请求，也没有timeout判断标准，之后加入
            timeoutCnt = 0
            allCnt = 1

    def _deltaTime(self):
        return time() - self.__tmstart

    def _dispatch(self, ctx, request, *args, **kwargs):
        self._unifyCacheTimeout = 0
        try:
            if request.body:
                jrequest = jloads(request.body.decode())
            else:
                jrequest = {}
        except JSONDecodeError as e:
            traceback.print_exc()
            #raise LogicErrorException('param json format error: %s' % str(e))
            jrequest = {}
        except UnicodeDecodeError as e:
            traceback.print_exc()
            jrequest = {}
        self.init(ctx)

        try:
            self.dolog('jrequest %s' % str(jrequest))
            params = self.unify_params(request, jrequest)
            self.dolog('unify_params %s' % str(params))
        except KeyError as e:
            traceback.print_exc()
            raise LogicErrorException('unify params not found %s' % str(e))

        if not ctx.nocache and self._unifyCacheTimeout > 0:
            unitfyCache = self._unifyCache(ctx=ctx, request=request, jrequest=jrequest, params=params, *args, **kwargs)
            if unitfyCache is not None:
                self.dolog('### got cache ###')
                return {'result': unitfyCache, 'cache': 1}

        result = self._json_internal(ctx=ctx, request=request, jrequest=jrequest,
                params=params, *args, **kwargs)

        if not ctx.nocache and self._unifyCacheTimeout > 0:
            unitfyCache = self._setUnifyCache(ctx=ctx, request=request,
                    jrequest=jrequest, params=params, result=result, *args, **kwargs)

        return {'result': result, 'cache': 0}

    def init(self, ctx):
        pass

    def _parse_ctx(self, request):
        apikey = request.META.get('HTTP_APIKEY', '0')
        apisecret = request.META.get('HTTP_APISECRET', '0')
        ctx = Context(apikey, apisecret)
        ctx.fillRequest(request)
        ctx.nocache = int(request.META.get('HTTP_NOCACHE', '0'))
        return ctx

    def unify_params(self, request, jrequest):
        return None

    @monit_time
    def _json_internal(self, *args, **kwargs):
        return self.json(*args, **kwargs)

    def json(self, ctx, request, jrequest, params, *args, **kwargs):
        raise NotImplementedError

    def setUnifyCache(self, timeout=900):
        self._unifyCacheTimeout = timeout

    def _unifyCache(self, ctx, request, jrequest, params, *args, **kwargs):
        key = self._unifyCacheKey(ctx, request, jrequest, params, *args, **kwargs)
        self.dolog('_unifyCache key(%s)' % key)
        rconn = self._unifyCacheRedisConn()
        res = rconn.get(key)
        if res: return jloads(res.decode('utf8'))
        else: return None

    def _setUnifyCache(self, ctx, request, jrequest, params, result, *args, **kwargs):
        key = self._unifyCacheKey(ctx, request, jrequest, params, *args, **kwargs)
        self.dolog('_setUnifyCache key(%s)' % key)
        rconn = self._unifyCacheRedisConn()
        rconn.set(key, jdumps(result).encode('utf8'), self._unifyCacheTimeout)

    def _unifyCacheRedisConn(self):
        from django_redis import get_redis_connection
        rconn = get_redis_connection("default") # redis5
        return rconn

    def _unifyCacheKey(self, ctx, request, jrequest, params, *args, **kwargs):
        paramhash = md5(request.body).hexdigest()
        key = '%s#%s#%s' % (request.path_info, ctx.source, paramhash)
        return key

    def dolog(self, msg):
        if RUNSERVER_MODE:
            ColorPrint.bold(msg)

class SimpleContext(object):
    def __init__(self):
        self.clientip = '127.0.0.1'
        self.serverip = '0.0.0.0'
        self.forcelog = 0
        self.clientname = 'Unknown'

    def fillRequest(self, request):
        self.clientip = get_client_ip(request)
        self.serverip = get_server_ip(request)

    def checkValid(self, withExcept):
        valid = True
        errmsg = 'Unknown error'
        if self.clientname == 'Unknown':
            valid = False
            errmsg = 'clientname(%s)' % self.clientname

        if not valid and withExcept:
            raise LogicErrorException(errmsg)
        return valid, errmsg

class SimpleJsonView(View):
    '''
    @brief: 带监控的 json view 基类
    @note: 无 cache token taf 特性, 无 Context 有效字段
    '''
    @method_decorator(block_json)
    @method_decorator(require_POST)
    def dispatch(self, request, *args, **kwargs):
        self.__tmstart = time()
        ctx = self._parse_ctx(request)
        resultInfo = {}
        try:
            successCnt = 0
            cacheStatus = 'unknown'
            resultInfo = self._dispatch(ctx, request, *args, **kwargs)
            successCnt += 1
            return resultInfo['result']
        finally:
            clientIp = ctx.clientip
            requestPath = request.path_info
            requestType = 'jsonapi'

            timeConsume = self._deltaTime()
            # 目前没有异步请求，也没有timeout判断标准，之后加入
            timeoutCnt = 0
            allCnt = 1

    def _deltaTime(self):
        return time() - self.__tmstart

    def _dispatch(self, ctx, request, *args, **kwargs):
        try:
            if request.body:
                jrequest = jloads(request.body.decode())
            else:
                jrequest = {}
        except JSONDecodeError as e:
            traceback.print_exc()
            raise LogicErrorException('param json format error: %s' % str(e))
        self.init(ctx)

        try:
            self.dolog('jrequest %s' % str(jrequest))
            params = self.unify_params(request, jrequest)
            self.dolog('unify_params %s' % str(params))
        except KeyError as e:
            traceback.print_exc()
            raise LogicErrorException('unify params not found %s' % str(e))

        result = self._json_internal(ctx=ctx, request=request, jrequest=jrequest, params=params, *args, **kwargs)

        return {'result': result, 'cache': 0}

    def init(self, ctx):
        pass

    def unify_params(self, request, jrequest):
        return None

    @monit_time
    def _json_internal(self, *args, **kwargs):
        return self.json(*args, **kwargs)

    def json(self, ctx, request, jrequest, params, *args, **kwargs):
        raise NotImplementedError

    def dolog(self, msg):
        if RUNSERVER_MODE:
            ColorPrint.bold(msg)

    def _parse_ctx(self, request):
        ctx = SimpleContext()
        ctx.fillRequest(request)
        ctx.forcelog = int(request.META.get('HTTP_FORCELOG', '0'))
        ctx.clientname = request.META.get('HTTP_CLIENTNAME', 'Unknown')
        return ctx
