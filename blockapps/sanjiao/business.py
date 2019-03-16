'''
Created on 2018年8月16日

@author: qiaoxiaofeng
'''
from blockuser.basequant import quantpolicy
import ccxt
from acom.utils.strutil import green, blue, red, dump
import asyncio
import uvloop
from blockdjcom.decorators import monit_time

class Sanjiao(quantpolicy):
    
    def __init__(self, exchange, symbol, accesskey, secretkey,\
                 base_volume, symbol1, symbol2, min_percent):
        super().__init__(exchange, symbol, accesskey, secretkey)
        self.symbol1 = symbol1
        self.symbol2 = symbol2
        self.base_volume = base_volume
        self.min_percent = min_percent
        self.instance = None
        self.markets = None
    
    def run(self):
        try:
            id = self.exchange
            # check if the exchange is supported by ccxt
            exchange_found = id in ccxt.exchanges
            if exchange_found:
                dump('Instantiating', green(id))
                exchange = getattr(ccxt, id)({
                    # 'proxy':'https://cors-anywhere.herokuapp.com/',
                    'apiKey': self.accesskey,
                    'secret': self.secretkey,
                    #'enableRateLimit': True,
                    })
                self.instance = exchange
                # load all markets from exchange
                self.markets = self.instance.load_markets()
                # output all symbols
                #dump(green(id), 'has', len(exchange.symbols), 'symbols:', green(', '.join(exchange.symbols))) 
                delay = int(exchange.rateLimit / 1000)  # delay in between requests
                # fetch ticker
                ticker = exchange.fetch_ticker(self.symbol)
#                 dump(green(id),
#                      green(self.symbol),
#                      'ticker',
#                      ticker['datetime'],
#                      'high: ' + str(ticker['high']),
#                      'low: ' + str(ticker['low']),
#                      'bid: ' + str(ticker['bid']),
#                      'bidVolume: ' + str(ticker['bidVolume']),
#                      'ask: ' + str(ticker['ask']),
#                      'askVolume: ' + str(ticker['askVolume']),
#                      'volume: ' + str(ticker['quoteVolume']))
                ticker1 = exchange.fetch_ticker(self.symbol1)
                '''
                dump(green(id),
                     green(self.symbol1),
                     'ticker1',
                     ticker1['datetime'],
                     'high: ' + str(ticker1['high']),
                     'low: ' + str(ticker1['low']),
                     'bid: ' + str(ticker1['bid']),
                     'bidVolume: ' + str(ticker1['bidVolume']),
                     'ask: ' + str(ticker1['ask']),
                     'askVolume: ' + str(ticker1['askVolume']),
                     'volume: ' + str(ticker1['quoteVolume']))
                '''
                
                ticker2 = exchange.fetch_ticker(self.symbol2)
                '''
                dump(green(id),
                     green(self.symbol2),
                     'ticker2',
                     ticker2['datetime'],
                     'high: ' + str(ticker2['high']),
                     'low: ' + str(ticker2['low']),
                     'bid: ' + str(ticker2['bid']),
                     'bidVolume: ' + str(ticker2['bidVolume']),
                     'ask: ' + str(ticker2['ask']),
                     'askVolume: ' + str(ticker2['askVolume']),
                     'volume: ' + str(ticker2['quoteVolume']))
                '''
                
                # don't check balance for speed
                ask1_price = ticker['ask']
                ask1_volume = ticker['askVolume']
                bid1_price = ticker['bid']
                bid1_volume = ticker['bidVolume']

                ask2_price = ticker1['ask']
                ask2_volume = ticker['askVolume']
                bid2_price = ticker1['bid']
                bid2_volume = ticker1['bidVolume']

                ask3_price = ticker2['ask']
                ask3_volume = ticker2['askVolume']
                bid3_price = ticker2['bid']
                bid3_volume = ticker2['bidVolume']
                
                #such as btc/usdt->eth/btc->eth/usdt
                percent_shun =  bid3_price / (ask1_price * ask2_price) * (1 - self.markets[self.symbol]['taker'])*(1 - self.markets[self.symbol1]['taker'])*(1 - self.markets[self.symbol2]['taker'])
                if percent_shun > 1:
                    print('shun: %s' % percent_shun)
                if percent_shun >= 1 + self.min_percent:
                    import ipdb;ipdb.set_trace()
                    # cal basevolume amount
                    basevolume_1 = ask1_price * ask1_volume   
                    basevolume_2 = ask2_price * ask2_volume * ask1_price /(1 - self.markets[self.symbol1]['taker'])
                    basevolume_3 = bid3_volume/(1 - self.markets[self.symbol2]['taker']) * ask2_price * ask1_price / (1-self.markets[self.symbol1]['taker'])
                    min_basevolume = min(basevolume_1, basevolume_2, basevolume_3)
                    if min_basevolume > self.base_volume:
                        #TODO: fix  小数点进位的问题
                        base_volume = round(self.base_volume, self.markets[self.symbol]['precision']['amount'])
                    else:
                        base_volume = round(min_basevolume, self.markets[self.symbol]['precision']['amount'])
                    # put order one by one
                    try:
                        volume1 = round(base_volume / ask1_price,self.markets[self.symbol]['precision']['amount'])
                        if volume1 > self.markets[self.symbol]['limits']['amount']['max'] or volume1 < self.markets[self.symbol]['limits']['amount']['min']:
                            return
                        response1 = self.instance.create_limit_buy_order(self.symbol, volume1, ask1_price)
                        order_id = response1['id']
                        order_status = self.instance.fetchOrder(order_id)
                        if order_status['status'] == 'open':
                            #TODO: fix me
                            volume1 = round(order_status['filled'] * (1-self.markets[self.symbol]['taker']), self.markets[self.symbol]['precision']['amount'])
                            try:
                                self.instance.cancelOrder(order_id)
                            except ccxt.OrderNotFound as e:
                                print('Failed to cancel order with', self.instance.id, type(e).__name__, str(e))
                            finally:
                                if int(volume1) == 0:
                                    return
                        elif order_status['status'] == 'canceled':
                            return
                        elif order_status['status'] == 'closed': 
                            volume1 = round(order_status['filled'] * (1-self.markets[self.symbol]['taker']), self.markets[self.symbol]['precision']['amount'])
                        volume2 = round(volume1 / ask2_price, self.markets[self.symbol1]['precision']['amount'])
                        if volume2 > self.markets[self.symbol1]['limits']['amount']['max'] or volume2 < self.markets[self.symbol1]['limits']['amount']['min']:
                            # 取消第一步的订单，卖出
                            # 此时会有卖出折价亏损
                            revert_response1 = self.instance.create_limit_sell_order(self.symbol, volume1, bid1_price)
                            return
                        response2 = self.instance.create_limit_buy_order(self.symbol1, volume2, ask2_price)
                        order_id = response2['id']
                        order_status = self.instance.fetchOrder(order_id)
                        if order_status['status'] == 'open':
                            # 取消全部订单，包括上一步订单,也就是全部卖出
                            try:
                                self.instance.cancelOrder(order_id)
                            except ccxt.OrderNotFound as e:
                                print('Failed to cancel order with', self.instance.id, type(e).__name__, str(e))
                            filled_volume = round(order_status['filled']*(1-self.markets[self.symbol1]['taker']), self.markets[self.symbol1]['precision']['amount']) 
                            if int(filled_volume) != 0 :
                                revert_response1 = self.instance.create_limit_sell_order(self.symbol1, filled_volume, bid2_price)
                            revert_response2 = self.instance.create_limit_sell_order(self.symbol, volume1, bid1_price)
                            return
                        elif order_status['status'] == 'closed':
                            volume2 = order_status['filled'] * (1-self.markets[self.symbol1]['taker'])
                        volume3 = round(volume2, self.markets[self.symbol]['precision']['amount'])
                        if volume3 > self.markets[self.symbol2]['limits']['amount']['max'] or volume3 < self.markets[self.symbol2]['limits']['amount']['min']:
                            # 取消第一步第二步订单，也就是全部卖出
                            revert_response1 = self.instance.create_limit_sell_order(self.symbol1, volume2, bid2_price)
                            revert_response2 = self.instance.create_limit_sell_order(self.symbol, volume1, bid1_price)
                            return
                        response3 = self.instance.create_limit_sell_order(self.symbol2, volume3, bid3_price)
                        order_id = response3['id']
                        order_status = self.instance.fetchOrder(order_id)
                        if order_status['status'] == 'open':
                            # 取消全部订单，包括上一步订单,也就是全部卖出
                            try:
                                self.instance.cancelOrder(order_id)
                            except ccxt.OrderNotFound as e:
                                print('Failed to cancel order with', self.instance.id, type(e).__name__, str(e))
                            filled_volume = round(order_status['filled']*(1-self.markets[self.symbol2]['taker']), self.markets[self.symbol2]['precision']['amount']) 
                            if int(filled_volume) != 0 :
                                revert_response3 = self.instance.create_limit_buy_order(self.symbol2, filled_volume, ask3_price)
                            revert_response2 = self.instance.create_limit_sell_order(self.symbol1, volume2, bid2_price)
                            revert_response1 = self.instance.create_limit_sell_order(self.symbol, volume1, bid1_price)
                            return
                        elif order_status['status'] == 'closed':
                            volume3 = order_status['filled']
                    except Exception as e:
                        print('Failed to create order with', self.instance.id, type(e).__name__, str(e))
                        response = None
                # reverse the sanjiao such as eth/usdt -> eth/btc --> btc/usdt
                percent_ni = bid2_price * bid1_price / ask3_price * (1 - self.markets[self.symbol]['taker'])*(1 - self.markets[self.symbol1]['taker'])*(1 - self.markets[self.symbol2]['taker'])
                if percent_ni>1:
                    print('ni:%s' % percent_ni)
                if percent_ni >= 1 + self.min_percent:
                    import ipdb;ipdb.set_trace()
                    # cal basevolume amount
                    basevolume_1 = ask3_price * ask3_volume
                    basevolume_2 = bid2_volume * ask3_price / (1 - self.markets[self.symbol2]['taker'])
                    basevolume_3 = bid1_volume/(1 - self.markets[self.symbol]['taker'])/bid2_price/(1 - self.markets[self.symbol2]['taker'])*ask3_price
                    min_basevolume = min(basevolume_1, basevolume_2, basevolume_3) 
                    if min_basevolume > self.base_volume:
                        base_volume = round(self.base_volume, self.markets[self.symbol2]['precision']['amount'])
                    else:
                        base_volume = round(min_basevolume, self.markets[self.symbol2]['precision']['amount'])
                # put order one by one
                    try:
                        volume1 = round(base_volume  / ask3_price, self.markets[self.symbol2]['precision']['amount'])
                        if volume1 > self.markets[self.symbol2]['limits']['amount']['max'] or volume1 < self.markets[self.symbol2]['limits']['amount']['min']:
                            return
                        response1 = self.instance.create_limit_buy_order(self.symbol2, volume1, ask3_price)
                        order_id = response1['id']
                        order_status = self.instance.fetchOrder(order_id)
                        if order_status['status'] == 'open':
                            #TODO: fix me
                            volume1 = round(order_status['filled']*(1 - self.markets[self.symbol2]['taker']) , self.markets[self.symbol2]['precision']['amount'])
                            try:
                                self.instance.cancelOrder(order_id)
                            except ccxt.OrderNotFound as e:
                                print('Failed to cancel order with', self.instance.id, type(e).__name__, str(e))
                            finally:
                                if int(volume1) == 0:
                                    return
                        elif order_status['status'] == 'canceled':
                            return
                        elif order_status['status'] == 'closed': 
                            volume1 = round(order_status['filled'] *(1 - self.markets[self.symbol2]['taker']), self.markets[self.symbol2]['precision']['amount']) 
                        volume2 = round(volume1, self.markets[self.symbol1]['precision']['amount'])
                        if volume2 > self.markets[self.symbol1]['limits']['amount']['max'] or volume2 < self.markets[self.symbol1]['limits']['amount']['min']:
                            # 取消第一步的订单，卖出
                            revert_response1 = self.instance.create_limit_sell_order(self.symbol2, volume1, bid3_price)
                            return
                        response2 = self.instance.create_limit_sell_order(self.symbol1, volume2, bid2_price)
                        order_id = response2['id']
                        order_status = self.instance.fetchOrder(order_id)
                        if order_status['status'] == 'open':
                            # 取消全部订单，包括上一步订单,也就是全部卖出
                            try:
                                self.instance.cancelOrder(order_id)
                            except ccxt.OrderNotFound as e:
                                print('Failed to cancel order with', self.instance.id, type(e).__name__, str(e))
                            filled_volume = round(order_status['filled']*(1-self.markets[self.symbol1]['taker']), self.markets[self.symbol1]['precision']['amount']) 
                            if int(filled_volume) != 0:
                                revert_response1 = self.instance.create_limit_buy_order(self.symbol1, filled_volume, ask2_price)
                            revert_response2 = self.instance.create_limit_sell_order(self.symbol2, volume1, bid3_price)
                            return
                        elif order_status['status'] == 'closed':
                            volume2 = round(order_status['filled'] * (1-self.markets[self.symbol2]['taker']),self.markets[self.symbol]['precision']['amount'])
                        volume3 = round(volume2, self.markets[self.symbol]['precision']['amount'])
                        if volume3 > self.markets[self.symbol2]['limits']['amount']['max'] or volume3 < self.markets[self.symbol2]['limits']['amount']['min']:
                            # 取消第一步第二步订单，也就是全部卖出
                            revert_response1 = self.instance.create_limit_buy_order(self.symbol1, volume2, ask2_price)
                            revert_response2 = self.instance.create_limit_sell_order(self.symbol2, volume1, bid3_price)
                            return
                        response3 = self.instance.create_limit_sell_order(self.symbol, volume3, bid1_price)
                        order_id = response3['id']
                        order_status = self.instance.fetchOrder(order_id)
                        if order_status['status'] == 'open':
                            # 取消全部订单，包括上一步订单,也就是全部卖出
                            try:
                                self.instance.cancelOrder(order_id)
                            except ccxt.OrderNotFound as e:
                                print('Failed to cancel order with', self.instance.id, type(e).__name__, str(e))
                            filled_volume = round(order_status['filled']*(1-self.markets[self.symbol]['taker']), self.markets[self.symbol]['precision']['amount']) 
                            if int(filled_volume) != 0:
                                revert_response3 = self.instance.create_limit_buy_order(self.symbol, filled_volume, ask1_price)
                            revert_response1 = self.instance.create_limit_buy_order(self.symbol1, volume2, ask2_price)
                            revert_response2 = self.instance.create_limit_sell_order(self.symbol2, volume1, bid3_price)
                            return
                        elif order_status['status'] == 'closed':
                            volume3 = order_status['filled'] * (1-self.markets[self.symbol]['taker'])
                    except Exception as e:
                        print('Failed to create order with', self.instance.id, type(e).__name__, str(e))
                        response = None
            else:
                dump('Exchange ' + (id) + ' not found')
        except ccxt.DDoSProtection as e:
            print(type(e).__name__, e.args, 'DDoS Protection (ignoring)')
        except ccxt.RequestTimeout as e:
            print(type(e).__name__, e.args, 'Request Timeout (ignoring)')
        except ccxt.ExchangeNotAvailable as e:
            print(type(e).__name__, e.args, 'Exchange Not Available due to downtime or maintenance (ignoring)')
        except ccxt.AuthenticationError as e:
            print(type(e).__name__, e.args, 'Authentication Error (missing API keys, ignoring)')