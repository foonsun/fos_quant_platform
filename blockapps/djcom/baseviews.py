from django.views.generic.base import TemplateView, View
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from .decorators import json_view
from django.conf import settings
from acom.utils.strutil import ColorPrint
from traceback import print_exc
from djcom.exceptions import LogicErrorException
from time import time
from json import loads as jloads
from json.decoder import JSONDecodeError

RUNSERVER_MODE = getattr(settings, 'RUNSERVER_MODE', False)

class Context(object):
    pass

class BaseTemplateView(TemplateView):
    def get(self, request, *args, **kwargs):
        self.fillview()
        return TemplateView.get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.fillview()
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def fillview(self):
        pass

class BaseJsonView(View):
    '''
    @brief: Json Post view base class
    '''
    @method_decorator(json_view)
    @method_decorator(require_POST)
    def dispatch(self, request, *args, **kwargs):
        self.__tmstart = time()
        resultInfo = {}
        ctx = Context()  # NOTE: not used now
        resultInfo = self._dispatch(ctx, request, *args, **kwargs)
        return resultInfo['result']

    def _deltaTime(self):
        return time() - self.__tmstart

    def _dispatch(self, ctx, request, *args, **kwargs):
        try:
            if request.body:
                jrequest = jloads(request.body.decode())
            else:
                jrequest = {}
        except JSONDecodeError as e:
            print_exc()
            errmsg = 'param json format error: %s\n%s' % (str(e), request.body)
            self.dolog(errmsg)
            raise LogicErrorException(errmsg)
        self.init(ctx)

        try:
            self.dolog('jrequest %s' % str(jrequest))
            params = self.unify_params(request, jrequest)
            self.dolog('unify_params %s' % str(params))
        except KeyError as e:
            print_exc()
            raise LogicErrorException('unify params not found %s' % str(e))

        result = self._json_internal(ctx=ctx, request=request, jrequest=jrequest, params=params, *args, **kwargs)

        return {'result': result, 'cache': 0}

    def init(self, ctx):
        pass

    def unify_params(self, request, jrequest):
        return None

    def _json_internal(self, *args, **kwargs):
        return self.json(*args, **kwargs)

    def json(self, ctx, request, jrequest, params, *args, **kwargs):
        raise NotImplementedError

    def dolog(self, msg):
        if RUNSERVER_MODE:
            ColorPrint.bold(msg)
