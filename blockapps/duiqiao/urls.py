from django.conf.urls import include, url
from .views import addDuiqiaoView, getDuiqiaoDetailView,\
                        getDuiqiaoListView, updateDuiqiaoView, deleteDuiqiaoView                     
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^manage/duiqiao/add/$', login_required(addDuiqiaoView.as_view()), name='manage_addduiqiao'),
    url(r'^manage/duiqiao/(?P<pk>[0-9]+)/update/$', login_required(updateDuiqiaoView.as_view()), name='manage_updateduiqiao'),
    url(r'manage/duiqiao/(?P<pk>[0-9]+)/delete/$', login_required(deleteDuiqiaoView.as_view()), name='manage_deleteduiqiao'),
    url(r'^manage/duiqiao/(?P<pk>[0-9]+)/$', login_required(getDuiqiaoDetailView.as_view()), name='manage_getduiqiao'),
    url(r'^manage/duiqiao/list/$', login_required(getDuiqiaoListView.as_view()), name='manage_getduiqiaolist'),
]
