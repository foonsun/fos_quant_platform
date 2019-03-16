from django.conf.urls import include, url
from blockuser.views import getQuantListView,getQuantDetailView,manageIndexView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^manage/index/$', login_required(manageIndexView.as_view()), name='manage_index'),
    url(r'^product/quantlist/$', getQuantListView.as_view(), name='product_getquantlist'),
    url(r'^product/quant/(?P<pk>[0-9]+)/$', getQuantDetailView.as_view(), name='product_getquantdetail'),
]
