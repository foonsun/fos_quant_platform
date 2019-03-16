from django.contrib.admin.sites import AdminSite as _AdminSite

from .forms import AdminAuthenticationForm
from djcom.utils import get_client_ip
from django.core.cache import cache
from django.contrib.auth.signals import user_logged_in

class AdminSite(_AdminSite):
    #login_form = AdminAuthenticationForm
    login_template = 'admin/captcha_login.html'

    @classmethod
    def GenCaptchaKey(cls, request):
        clientip = get_client_ip(request)
        key = 'login-captcha-count-%s' % clientip
        return key

    def login(self, request, extra_context=None):
        key = AdminSite.GenCaptchaKey(request)
        count = int(cache.get(key, 0))
        if count < 3:
            self.login_form = None
        else:
            self.login_form = AdminAuthenticationForm
        if request.method == 'POST':
            cache.set(key, count+1, 30)
        return super(AdminSite, self).login(request, extra_context)

def logged_clean_captcha_cache(sender, request, user, **kwargs):
    key = AdminSite.GenCaptchaKey(request)
    cache.delete(key)

user_logged_in.connect(logged_clean_captcha_cache)
