from django.conf.urls import include, url
from oscar_accounts.dashboard.app import application as accounts_app
from oscarapi.app import application as api
from paypal.express.dashboard.app import application as express
from blockoscar.business import application

urlpatterns = [
    url(r'', application.urls),
    url(r'^dashboard/accounts/', accounts_app.urls),
    url(r'^api/', api.urls),
    url(r'^checkout/paypal/', include('paypal.express.urls')),
    # Optional
    url(r'^dashboard/paypal/express/', express.urls),
]
