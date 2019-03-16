"""blockserver URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.views.generic import TemplateView
#from oscar.app import application
from oscar.views import handler403, handler404, handler500

admin.autodiscover()

urlpatterns = staticfiles_urlpatterns()
urlpatterns += [
    url(r'^i18n/', include('django.conf.urls.i18n')),
    # Oscar's normal URLs
    #url(r'^', application.urls),
    url(r'', include('blockoscar.urls')),
    url(r'', include('blockuser.urls')),
    url(r'', include('sanjiao.urls')),
    url(r'', include('duiqiao.urls')),
    url(r'^eBlockTst_admin123/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^captcha/', include('captcha.urls')),
    #url(r'^chat/', include('chat.urls')),
    ]

urlpatterns += [
]
if settings.DEBUG:
        import debug_toolbar
        urlpatterns += [ url(r'^__debug__/', include(debug_toolbar.urls)),]
        urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
        urlpatterns += [
            url(r'^403$', handler403, {'exception': Exception()}),
            url(r'^404$', handler404, {'exception': Exception()}),
            url(r'^500$', handler500),
    ]
