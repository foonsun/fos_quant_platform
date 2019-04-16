from django.conf.urls import include, url
from .views import addLimitBuyView, getLimitBuyDetailView,\
                        getLimitBuyListView, updateLimitBuyView, deleteLimitBuyView                     
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^manage/limitbuy/add/$', login_required(addLimitBuyView.as_view()), name='manage_addlimitbuy'),
    url(r'^manage/limitbuy/(?P<pk>[0-9]+)/update/$', login_required(updateLimitBuyView.as_view()), name='manage_updatelimitbuy'),
    url(r'manage/limitbuy/(?P<pk>[0-9]+)/delete/$', login_required(deleteLimitBuyView.as_view()), name='manage_deletelimitbuy'),
    url(r'^manage/limitbuy/(?P<pk>[0-9]+)/$', login_required(getLimitBuyDetailView.as_view()), name='manage_getlimitbuy'),
    url(r'^manage/limitbuy/list/$', login_required(getLimitBuyListView.as_view()), name='manage_getlimitbuylist'),
]
