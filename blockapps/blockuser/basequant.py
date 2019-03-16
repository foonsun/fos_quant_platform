'''
Created on 2018年8月16日

@author: qiaoxiaofeng
'''
class quantpolicy(object):

    def __init__(self, exchange, symbol, accesskey, secretkey):
        self.exchange = exchange
        self.symbol = symbol
        self.accesskey = accesskey
        self.secretkey = secretkey