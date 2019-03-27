from django.conf.urls import *
from django.views.decorators.csrf import csrf_exempt
from . import views


urlpatterns = [
   url(r'^respond$', views.ResponseView.as_view(),
        name='payjs-weixin-answer'),#回调函数
]
