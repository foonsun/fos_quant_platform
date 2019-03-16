# -*- coding:utf-8 -*-

import base64
import hashlib
import hmac
import json
import time
from urllib import parse
import requests

class baseFcoin(object):
    def __init__(self, public_key, secret_key):
        self.public_key = public_key
        self.secret_key = secret_key

    access_url = 'https://api.fcoin.com/v2/'
    url = 'https://api.fcoin.com/v2/'
    headers = {
        'content-type': 'application/json;charset=UTF-8',
    }
    # 获取最新的成交明细
    def get_market_orders(self, symbol, limit, before):
        suf = 'market/trades/' + symbol
        payload = {'limit': limit, 'before': before}	
        result = requests.get(self.url + suf, params=payload)
        return result.json()	    

    # 获取ticker
    def get_market_ticker(self, symbol):
        suf = 'market/ticker/' + symbol
        result = requests.get(self.url + suf)
        return result.json()

    # 获取深度
    def get_market_depth(self, symbol, level ):
        suf = 'market/depth/' + level + '/' + symbol
        result = requests.get(self.url + suf)
        return result.json()

    # 获取蜡烛图
    def get_market_candles(self, symbol, level):
        suf = 'market/candles/' + level + '/' + symbol
        result = requests.get(self.url + suf)
        return result.json()

    # 获取用户资产
    def get_balance(self):
        suf = 'accounts/balance'
        t = time.time()
        TIMESTAMP = str(int(round(t * 1000)))
        self.create_headers('GET', self.access_url + suf, TIMESTAMP, '', self.public_key, self.secret_key)
        r = requests.get(self.url + suf, headers=self.headers)
        return r.json()

    # 创建新的订单
    '''
    symbol		交易对
    type		订单类型
    price		价格
    amount		下单量
    '''

    def create_order(self, symbol, side, order_type, price, amount):
        suf = 'orders'
        payload = {
            'symbol': symbol,
            'side': side,
            'type': order_type,
            'price': price,
            'amount': amount
        }
        print(payload)
        if order_type == 'market':
            del payload['price']
        TIMESTAMP = int(round(time.time() * 1000))
        self.create_headers('POST', self.access_url + suf, TIMESTAMP, payload, self.public_key, self.secret_key)
        r = requests.post(self.url + suf, data=json.dumps(payload), headers=self.headers)
        return r.json()


    # 获取订单列表
    '''
    symbol		交易对
    types		订单类型
    before		时间戳
    after		时间戳
    limit		每页的订单数量，默认为 20 条
    states		订单状态（submitted, partial_filled, partial_canceled, filled, canceled）
    '''

    def get_orders_list(self, symbol, states, before, after, limit):
        suf = 'orders'
        payload = {
            'symbol': symbol,
            'states': states,
            'before': before,
            'after': after,
            'limit': limit
        }
        #if states == '':
        #    del payload['states']
        if before == '':
            del payload['before']
        if after == '':
            del payload['after']
        if limit == '':
            del payload['limit']
        url_suf = '%s%s%s' % (self.access_url + suf, '?', self.sort_payload(payload))

        TIMESTAMP = str(int(round(time.time() * 1000)))
        self.create_headers('GET', url_suf, TIMESTAMP, '', self.public_key, self.secret_key)
        r = requests.get(self.url + suf, params=payload, headers=self.headers)
        return r.json()


    # 获取指定订单
    '''
    order_id	需要获取的订单的 ID
    '''

    def get_order_by_id(self, order_id):
        suf = 'orders/' + str(order_id)
        TIMESTAMP = str(int(round(time.time() * 1000)))
        self.create_headers('GET', self.access_url + suf, TIMESTAMP, '', self.public_key, self.secret_key)
        r = requests.get(self.url + suf, headers=self.headers)
        return r.json()

    # 申请撤销订单
    def cancel_order(self, order_id):
        suf = 'orders/' + str(order_id) + '/submit-cancel'
        TIMESTAMP = str(int(round(time.time() * 1000)))
        self.create_headers('POST', self.access_url + suf, TIMESTAMP, '', self.public_key, self.secret_key)
        r = requests.post(self.url + suf, headers=self.headers)
        return r.json()

    # 查询指定订单的成交记录
    def get_result_by_id(self, order_id):
        suf = 'orders/' + str(order_id) + '/match-results'
        TIMESTAMP = str(int(round(time.time() * 1000)))
        self.create_headers('GET', self.access_url + suf, TIMESTAMP, '', self.public_key, self.secret_key)
        r = requests.get(self.url + suf, headers=self.headers)
        return r.json()

    def sort_payload(self, payload):
        keys = sorted(payload.keys())
        result = ''
        for i in range(len(keys)):
            if i != 0:
                result += '&' + keys[i] + "=" + str(payload[keys[i]])
            else:
                result += keys[i] + "=" + str(payload[keys[i]])
        return result

    # 对请求数据进行加密编码
    def encrypt_data(self, HTTP_METHOD, HTTP_REQUEST_URI, TIMESTAMP, POST_BODY, secret):
        payload_result = ''
        if POST_BODY != '':
            payload_result = self.sort_payload(POST_BODY)
        data = HTTP_METHOD + HTTP_REQUEST_URI + TIMESTAMP + payload_result
        # print(data)
        data_base64 = base64.b64encode(bytes(data, encoding='utf8'))
        # print(data_base64)
        data_base64_sha1 = hmac.new(bytes(secret, encoding='utf8'), data_base64, hashlib.sha1).digest()
        data_base64_sha1_base64 = base64.b64encode(data_base64_sha1)
        # print(data_base64_sha1_base64)
        return str(data_base64_sha1_base64, encoding='utf-8')

    def create_headers(self, HTTP_METHOD, HTTP_REQUEST_URI, TIMESTAMP, POST_BODY, public_key, secret_key):
        signature = self.encrypt_data(HTTP_METHOD, HTTP_REQUEST_URI, str(TIMESTAMP), POST_BODY, secret_key)
        self.headers['FC-ACCESS-KEY'] = public_key
        self.headers['FC-ACCESS-TIMESTAMP'] = str(TIMESTAMP)
        self.headers['FC-ACCESS-SIGNATURE'] = signature

if __name__ == '__main__':
    publickey='46dac3feca2e4d01926309a0ea6aa0fd'
    seckey='d4e238b00e3e4f92b5ee4391c0dab5fa'
    fcoin=Fcoin(publickey,seckey)
    symbol='btcusdt'
    side='buy'
    order_type='limit'
    price='1'
    amount='1'
    fcoin.create_order(symbol, side, order_type, price, amount)
