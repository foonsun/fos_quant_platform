#######################################################################################
# 支付重定向:RedirectView
# 提交订单，向支付宝请求:ResponseView
# 支付宝回馈信息处理接口 ResponseView
# 取消订单 CancelView
# 该接口对应的支付源类型为:TaoBao_Warrant,需要在source_type里面添加该源类型
#######################################################################################
from django.views.generic import RedirectView, View,TemplateView
from payjs.conf import BASIC_PARAMS
from django.utils import six
import logging
import json
from payjs.gatewayinfo import Payjs
from payjs.exceptions import *
from django.conf import settings
from django.contrib.sites.models import Site
from django.http import HttpResponseRedirect,HttpResponse
from oscar.apps.checkout.mixins import RedirectSessionMixin
from oscar.core.loading import get_class, get_classes, get_model
PaymentDetailsView = get_class('checkout.views', 'PaymentDetailsView')
CheckoutSessionMixin = get_class('checkout.session', 'CheckoutSessionMixin')
OrderPlacementMixin = get_class('checkout.mixins', 'OrderPlacementMixin')
RedirectRequired, UnableToTakePayment, PaymentError \
    = get_classes('payment.exceptions', ['RedirectRequired',
                                         'UnableToTakePayment',
                                         'PaymentError'])
UnableToPlaceOrder = get_class('order.exceptions', 'UnableToPlaceOrder')
ShippingAddress = get_model('order', 'ShippingAddress')
Country = get_model('address', 'Country')
Basket = get_model('basket', 'Basket')
Repository = get_class('shipping.repository', 'Repository')
Applicator = get_class('offer.utils', 'Applicator')
Selector = get_class('partner.strategy', 'Selector')
Source = get_model('payment', 'Source')
SourceType = get_model('payment', 'SourceType')
logger = logging.getLogger('oscar.checkout')
from django.core.urlresolvers import reverse


class PayjsSessionMixin(RedirectSessionMixin):
    '''
    针对payjs支付方式的session管理控件，该控件对checkout_session进行管理，
    checkout_session是django-oscar的session管理控件，在支付完成后可以被自动清理。
    '''
    def set_payjs(self):
        params={key:BASIC_PARAMS[key] for key in BASIC_PARAMS if BASIC_PARAMS[key] !=None}
        payjs_gate=Payjs(**params)
        self.checkout_session._set('payjs','weixin',payjs_gate)
    def get_payjs(self):
        return self.checkout_session._get('payjs','weixin')

def PayjsHandle(paymentview, order_number, **kwargs):
    '''
    处理PAYJS请求
    '''
        # 获取支付url
        # setting
    payjs=PayjsSessionMixin(paymentview.checkout_session)
    if settings.DEBUG:
            # Determine the localserver's hostname to use when
            # in testing mode8
            base_url = 'http://%s' % paymentview.request.META['HTTP_HOST']
    else:
            base_url = 'https://%s' % Site.objects.get_current().domain

    submission=payjs.get_info()
    gateway_info={
        'total_fee':submission.get('order_total').incl_tax * 100,
        'body':submission['order_kwargs']['subject'],
        'out_trade_no':order_number,
         }
    gateway_info={key:gateway_info[key] for key in gateway_info if gateway_info[key]!=None}
    payjs.set_payjs()
    res = payjs.get_payjs().QRPay(**gateway_info)
    result = json.loads(res.content)
    if result['return_code']:
        url = res.qrcode
        print(url)
        raise RedirectRequired(url)
    else:
        print('get qrcode error')
        raise PaymentError('支付网关错误，请重试')

class ResponseView(PayjsSessionMixin,OrderPlacementMixin,View):
    '''
    收到payjs信息处理，notify_url
    '''
    def paid_order_create(self, request, payjs_info, *args, **kwargs):
        order_number=self.get_order_number()
        info=self.get_info()
        info.pop('payment_kwargs')
        info.pop('order_kwargs')
        info['order_number']=order_number
        info['user']=self.request.user
        info['basket']=self.get_submitted_basket()

        #info['shipping_address']=taobao_info['receive_name']+','\
        #                         +taobao_info['receive_address']+','\
        #                         +taobao_info['receive_zip']

        # Assign strategy to basket instance
        if Selector:
            info['basket'].strategy = Selector().strategy(self.request)

        # Re-apply any offers
        #Applicator().apply(info['basket'],self.request.user,self.request )

        # Record payment source
        source_type, is_created = SourceType.objects.get_or_create(name='payjs_weixin')
        source = Source(source_type=source_type,
                        currency=info['order_total'].currency,
                        amount_allocated=info['order_total'].incl_tax,
                        amount_debited=info['order_total'].incl_tax)
        self.add_payment_source(source)
        self.add_payment_event('paid', info['order_total'].incl_tax,reference=payjs_info['out_trade_no'])

        #添加订单
        return self.handle_order_placement(**info)

    def post(self, request, *args, **kwargs):
        #获取淘宝交易信息,notify_url
        payjs_gate=self.get_payjs()
        try:
            if payjs_gate.verify_notify(**request.POST):
                payjs_info=request.POST
                info=self.get_info()
                if(info.get('order_total').incl_tax * 100 != payjs_info.get('total_fee')):
                    raise InvalidInfoException
                self.paid_order_create(request,payjs_info, *args, **kwargs)
                return HttpResponse('success')
            else:
                raise InvalidInfoException
        except Exception as e:
            return HttpResponse ("fail")
