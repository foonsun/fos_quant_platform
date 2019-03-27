#######################################################################################
# payjs网关:
# 生成请求url，验证微信支付信息
#######################################################################################

import requests
import hashlib
from urllib.parse import urlencode, unquote_plus
from .exceptions import *

def ksort(d):
    return [(k, d[k]) for k in sorted(d.keys())]

class Payjs(object):
    def __init__(self, merchant_id, merchant_key, notify_url, **kwargs):
        self.merchant_key = merchant_key  # 填写通信密钥
        self.merchant_id = merchant_id  # 特写商户号
        self.notify_url = notify_url

    def curl(self, data, url):
        data['sign'] = self.sign(data)
        r = requests.post(url, data=data)
        return r

    def sign(self, attributes):
        attributes = ksort(attributes)
        m = hashlib.md5()
        m.update((unquote_plus(urlencode(attributes)) + '&key=' + self.merchant_key).encode(encoding='utf-8'))
        sign = m.hexdigest()
        sign = sign.upper()
        return sign

    def QRPay(self, total_fee, body, out_trade_no):
        url = 'https://payjs.cn/api/native'
        data = {}
        data['mchid'] = self.merchant_id
        data['total_fee'] = total_fee
        data['body'] = body
        data['out_trade_no'] = out_trade_no
        data['notify_url'] = self.notify_url
        return self.curl(data, url)

    def JSPay(self, total_fee, body, out_trade_no, callback_url=None):
        url = 'https://payjs.cn/api/jspay'
        data = {}
        data['mchid'] = self.merchant_id
        data['total_fee'] = total_fee
        data['body'] = body
        data['out_trade_no'] = out_trade_no
        # data['notify_url'] = self.notify_url
        if callback_url:
            data['callback_url'] = callback_url
        return self.curl(data, url)

    def Cashier(self, total_fee, body, out_trade_no, callback_url=None):
        url = 'https://payjs.cn/api/cashier'
        data = {}
        data['mchid'] = self.merchant_id
        data['total_fee'] = total_fee
        data['body'] = body
        data['out_trade_no'] = out_trade_no
        # data['notify_url'] = self.notify_url
        if callback_url:
            data['callback_url'] = callback_url
        return self.curl(data, url)

    def Query(self, payjs_order_id):
        url = 'https://payjs.cn/api/check'
        data = {}
        data['payjs_order_id'] = payjs_order_id
        return self.curl(data, url)
    
    def check_signature(self, data):
        """
        校验签名，签名不通过会抛出 InvalidSignature 异常
       :param key: 商户密钥
       :param data: 要签名的参数字典
       :param sign: 要校验的签名，省略（为 None）则从 data 中取 sign 字段
       :rtype: bool
        """
        if data['return_code']:
            sign = data.pop('sign')
            
            if self.sign(self.merchant_key, data) == sign:
                return True
        raise InvalidSignatureException