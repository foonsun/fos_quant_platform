#encoding=utf8
from __future__ import absolute_import, unicode_literals

import sys
from time import time
import logging
import traceback
from functools import wraps
from importlib import import_module

from django import http
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.core.handlers.base import BaseHandler
from django.core.serializers.json import DjangoJSONEncoder
from django.core.signals import got_request_exception
from django.utils import six, timezone
from django.utils.module_loading import import_string
from django.core.cache.backends.base import InvalidCacheBackendError

from acom.utils.strutil import ColorPrint, bytesToStr
from blockcomm.net.exceptions import BlockException, Exc_LogicAssertException,\
    LogicErrorException
from django_redis import get_redis_connection

json = import_module(getattr(settings, 'JSON_MODULE', 'json'))
JSON = getattr(settings, 'JSON_DEFAULT_CONTENT_TYPE', 'application/json; charset=utf-8')
logger = logging.getLogger('django.request')

class FormalJSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return bytesToStr(obj)
        return DjangoJSONEncoder.default(self, obj)

def _dump_json(data, indent=None, utf8=True):
    options = getattr(settings, 'JSON_OPTIONS', {})

    # Use the FormalJSONEncoder by default, unless cls is set to None.
    options.setdefault('cls', FormalJSONEncoder)
    if isinstance(options['cls'], six.string_types):
        options['cls'] = import_string(options['cls'])
    elif options['cls'] is None:
        options.pop('cls')
    if indent:
        options['indent'] = indent
    if utf8:
        options['ensure_ascii'] = False
        return json.dumps(data, **options).encode('utf8')
    else:
        return json.dumps(data, **options)

def block_json(*args, **kwargs):
    """Ensure the response content is well-formed JSON.
    Views wrapped in @json_view can return JSON-serializable Python objects,
    like lists and dicts, and the decorator will serialize the output and set
    the correct Content-type.
    Views may also throw known exceptions, like Http404, PermissionDenied, etc,
    and @json_view will convert the response to a standard JSON error format,
    and set the status code and content type.
    If you return a two item tuple, the first is a JSON-serializable object and
    the second is an integer used for the HTTP status code, e.g.:
    >>> @json_view
    ... def example(request):
    ...    return {'foo': 'bar'}, 418
    By default all responses will get application/json as their content type.
    You can override it for non-error responses by giving the content_type
    keyword parameter to the decorator, e.g.:
    >>> @json_view(content_type='application/vnd.example-v1.0+json')
    ... def example2(request):
    ...     return {'foo': 'bar'}
    """

    content_type = kwargs.get('content_type', JSON)

    def decorator(f):
        @wraps(f)
        def _wrapped(request, *a, **kw):
            try:
                status = 200
                headers = {}
                ret = f(request, *a, **kw)

                if isinstance(ret, tuple):
                    if len(ret) == 3:
                        ret, headers, status = ret
                    else:
                        ret, headers = ret

                # Some errors are not exceptions. :\
                if isinstance(ret, http.HttpResponseNotAllowed):
                    blob = _dump_json({
                        'code': -1,
                        'timestamp': int(time() * 1000),
                        'error': 405,
                        'message': 'HTTP method not allowed.'
                    })
                    # debugging information
                    logger.error(
                        'Internal Server Error: %s', request.path,
                        exc_info=True,
                        extra={
                            'code': -1,
                            'timestamp': int(time() * 1000),
                            'status_code': 405,
                            'request': request,
                        })
                    return http.HttpResponse(
                        blob, status=405, content_type=JSON)

                # Allow HttpResponses to go straight through.
                if isinstance(ret, http.HttpResponse):
                    return ret

                data = {'code': 0,
                        'timestamp': int(time() * 1000),
                        'message': 'Success',
                        'data': ret}
                data.update(headers)
                blob = _dump_json(data)
                print(_dump_json(data, utf8=False)[:100])
                assert(type(status) is int)
                response = http.HttpResponse(blob, status=status,
                                             content_type=content_type)
                for k in headers:
                    response[k] = headers[k]
                return response
            except http.Http404 as e:
                traceback.print_exc()
                blob = _dump_json({
                    'code': -1,
                    'timestamp': int(time() * 1000),
                    'error': 404,
                    'message': six.text_type(e),
                })
                logger.error('not found: %s', request.path,
                               extra={
                                   'code': -1,
                                   'timestamp': int(time() * 1000),
                                   'status_code': 404,
                                   'request': request,
                               })
                return http.HttpResponseNotFound(blob, content_type=JSON)
            except PermissionDenied as e:
                traceback.print_exc()
                logger.error(
                    'Forbidden (Permission denied): %s', request.path,
                    extra={
                        'code': -1,
                        'timestamp': int(time() * 1000),
                        'status_code': 403,
                        'request': request,
                    })
                blob = _dump_json({
                    'code': -1,
                    'timestamp': int(time() * 1000),
                    'error': 403,
                    'message': six.text_type(e),
                })
                return http.HttpResponseForbidden(blob, content_type=JSON)
            except BlockException as e:
                traceback.print_exc()
                blob = _dump_json({
                    'code': e.code,
                    'timestamp': int(time() * 1000),
                    'error': 400,
                    'message': six.text_type(e),
                })
                # Generate the usual 500 error email with stack trace and full
                # debugging information
                logger.error(
                    'Internal Server Error: %s', request.path,
                    exc_info=True,
                    extra={
                        'code': -1,
                        'timestamp': int(time() * 1000),
                        'status_code': 400,
                        'request': request,
                    })
                return http.HttpResponseBadRequest(blob, content_type=JSON)
            except Exception as e:
                traceback.print_exc()
                exc_data = {
                    'code': -1,
                    'timestamp': int(time() * 1000),
                    'error': 500,
                    'message': 'An error occurred',
                }
                if settings.DEBUG:
                    exc_data['message'] = six.text_type(e)
                    exc_data['traceback'] = traceback.format_exc()

                blob = _dump_json(exc_data)

                # Generate the usual 500 error email with stack trace and full
                # debugging information
                logger.error(
                    'Internal Server Error: %s', request.path,
                    exc_info=True,
                    extra={
                        'code': -1,
                        'timestamp': int(time() * 1000),
                        'status_code': 500,
                        'request': request,
                    }
                )

                # Here we lie a little bit. Because we swallow the exception,
                # the BaseHandler doesn't get to send this signal. It sets the
                # sender argument to self.__class__, in case the BaseHandler
                # is subclassed.
                got_request_exception.send(sender=BaseHandler, request=request)
                return http.HttpResponseServerError(blob, content_type=JSON)
        return _wrapped
    if len(args) == 1 and callable(args[0]):
        return decorator(args[0])
    else:
        return decorator

def verify_ctx_required(*args, **kwargs):
    def decorator(f):
        @wraps(f)
        def _wrapped(self, *a, **kw):
            ctx = kw.get('ctx', None)
            Exc_LogicAssertException(ctx is not None, 'ctx should not be None')
            ctx.checkValid(True)
            return f(self, *a, **kw)
        return _wrapped
    if len(args) == 1 and callable(args[0]):
        return decorator(args[0])
    else:
        return decorator

def unify_params(*args, **kwargs):
    def decorator(f):
        @wraps(f)
        def _wrapped(self, *a, **kw):
            Exc_LogicAssertException(kw.get('params', None) is not None,
                                     'unify_params params should not be None')
            return f(self, *a, **kw)
        return _wrapped
    if len(args) == 1 and callable(args[0]):
        return decorator(args[0])
    else:
        return decorator

from django_redis import get_redis_connection
try:
    monit_conn = get_redis_connection('redis6')
except InvalidCacheBackendError as e:
    #raise Exc_LogicAssertException(None,'redis monitor hook: can not connect to redis6 error!')
    sys.stderr.write('can not use monit_time redis log')
    monit_conn = None


def redis_monitor_hook(requestPath, limittm, timeConsume, descext, *args, **kwargs):
    ColorPrint.underline('deltatm(%.3f) %s ' % (timeConsume, requestPath))
    if timeConsume < limittm:
        # no log needed, return directly
        return
    desc = {}
    desc['deltatm'] = int(timeConsume)
    desc['limittm'] = limittm
    desc['time'] = timezone.datetime.now().strftime('%Y%m%d-%H:%M:%S')
    desc.update(descext)
    ColorPrint.invert('slow %s %s' % (requestPath, _dump_json(desc, utf8=False)[:100]))
    if monit_conn:
        monit_conn.rpush('monit_time-%s' % requestPath, desc)

def monit_time(*args, **kwargs):
    def decorator(f):
        @wraps(f)
        def _wrapped(self, *a, **kw):
            limittm = kwargs.get('monit_limit', None)
            if not limittm:
                limittm = int(getattr(self, 'monit_limit', 3))
            starttm = time()
            result = f(self, *a, **kw)
            deltatm = time()-starttm

            name = kwargs.pop('name', None)
            if name is None:
                name = self.__class__.__module__+'.'+self.__class__.__name__+'::'+f.__name__

            descext = {}
            params = kw.get('params', None)
            if params is not None:
                descext['params'] = params
            else:
                jrequest = kw.get('jrequest', None)
                descext['jrequest'] = jrequest
            try:
                redis_monitor_hook(requestPath=name, limittm=limittm, timeConsume=deltatm, descext=descext)
            except Exception as e:
                traceback.print_exc()

            return result
        return _wrapped
    if len(args) == 1 and callable(args[0]):
        return decorator(args[0])
    else:
        return decorator

def access_limit(key_prefix, seconds, limit, *args, **kwargs):
    def decorator(f):
        @wraps(f)
        def _wrapped(self, *a, **kw):
            ctx = kw.get('ctx', None)
            key = '%s#%s' % (key_prefix, ctx.clientip)
            rconn = get_redis_connection("default") # redis5
            res = rconn.get(key)
            if not res:
                rconn.set(key, limit-1, seconds)
                return f(self, *a, **kw)
            elif int(res):
                rconn.decr(key)
                return f(self, *a, **kw)
            else:
                return None
        return _wrapped
    return decorator
