from django import http
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http.response import Http404
from json import dumps as jdumps, loads as jloads
import traceback
from datetime import datetime

class JSONServiceError(Exception):
    def __init__(self, detail, status_code=400):
        self.detail = detail
        self.status_code = status_code

class UtilMixin:
    def param(self, key, default=None, throw=False):
        if self.request.method == 'POST':
            result = self.request.POST.get(key, default)
        elif self.request.method == 'GET':
            result = self.request.GET.get(key, default)
        else:
            raise Http404('Unknown method %s' % self.request.method)
        if throw and result == default: raise Http404('Can not get parameter %s' % key)
        return result

class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)

class JSONServiceMixin(object):
    def get(self, request, *args, **kwargs):
        return self._json('get', request, self.request.GET, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self._json('post', request, jloads(request.body), *args, **kwargs)

    def _json(self, method, request, jrequest, *args, **kwargs):
        response = {'status': 500, 'detail': '', 'timestamp': datetime.now().strftime('%Y%m%d %H:%M:%S.%f'), 'data': {}}
        try:
            respdata = None
            if hasattr(self, 'service'):
                respdata = self.service(request, jrequest)
            elif method == 'get':
                respdata = self.service_get(request, jrequest)
            elif method == 'post':
                respdata = self.service_post(request, jrequest)
            if isinstance(respdata, http.HttpResponse):
                return respdata
            elif respdata is None:
                response['status'] = 200
            elif type(respdata) in (str, unicode):
                response['status'] = 200
                response['data'] = jloads(respdata)
            elif type(respdata) != dict:
                raise Exception('Can not return an type not as dict')
            else:
                response['status'] = 200
                response['data'] = respdata
            content = jdumps(response)
            kw = {'status': response['status']}
        except JSONServiceError as exc:
            traceback.print_exc()
            kw = {'status': exc.status_code}
            content = jdumps({'detail': exc.detail, 'status': exc.status_code})
        except Exception as exc:
            traceback.print_exc()
            kw = {'status': getattr(exc, 'status_code', 400)}
            content = jdumps({'detail': exc, 'status': kw['status']})

        return http.HttpResponse(content, content_type = 'application/json', **kw)

    #def service(self, request, jrequest): return {}
    def service_post(self): return {}
    def service_get(self): return {}

class JSONTemplateView(TemplateView, JSONServiceMixin):
    http_method_names = ['get', 'post']
    def get(self, request, *args, **kwargs):
        if request.META['CONTENT_TYPE'] == 'application/json':
            # json request
            return JSONServiceMixin.get(self, request, *args, **kwargs)
        else:
            # html request
            if hasattr(self, 'gethtml'): self.gethtml(request, *args, **kwargs)
            return TemplateView.get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.META['CONTENT_TYPE'] == 'application/json':
            # json request
            return JSONServiceMixin.post(self, request, *args, **kwargs)
        else:
            # html request
            if hasattr(self, 'posthtml'): self.posthtml(request, *args, **kwargs)
            context = self.get_context_data(**kwargs)
            return self.render_to_response(context)

class JSONResponseMixin(object):
    def render_to_response(self, context):
        "Returns a JSON response containing 'context' as payload"
        return self.get_json_response(self.convert_context_to_json(context))

    def get_json_response(self, content, **httpresponse_kwargs):
        "Construct an `HttpResponse` object."
        return http.HttpResponse(content,
                                 content_type='application/json',
                                 **httpresponse_kwargs)

    def convert_context_to_json(self, context):
        "Convert the context dictionary into a JSON object"
        # Note: This is *EXTREMELY* naive; in reality, you'll need
        # to do much more complex handling to ensure that arbitrary
        # objects -- such as Django model instances or querysets
        # -- can be serialized as JSON.
        return jdumps(context)

