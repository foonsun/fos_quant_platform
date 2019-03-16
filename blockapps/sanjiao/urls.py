from django.conf.urls import include, url
from .views import addSanjiaoView, updateSanjiaoView, deleteSanjiaoView, getSanjiaoDetailView, \
                        getSanjiaoListView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^manage/sanjiao/add/$', login_required(addSanjiaoView.as_view()), name='manage_addsanjiao'),
    url(r'^manage/sanjiao/(?P<pk>[0-9]+)/update/$', login_required(updateSanjiaoView.as_view()), name='manage_updatesanjiao'),
    url(r'manage/sanjiao/(?P<pk>[0-9]+)/delete/$', login_required(deleteSanjiaoView.as_view()), name='manage_deletesanjiao'),
    url(r'^manage/sanjiao/(?P<pk>[0-9]+)/$', login_required(getSanjiaoDetailView.as_view()), name='manage_getsanjiao'),
    url(r'^manage/sanjiao/list/$', login_required(getSanjiaoListView.as_view()), name='manage_getsanjiaolist'),
]