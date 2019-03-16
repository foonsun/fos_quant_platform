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

class DuiQiao(quantpolicy):
    
    def __init__(self, exchange, symbol, accesskey, secretkey,\
                 max_buy_price, min_sell_price, base_volume):
        super().__init__(exchange, symbol, accesskey, secretkey)
        self.max_buy_price = max_buy_price
        self.min_sell_price = min_sell_price
        self.base_volume = base_volume
        self.instance = None
    
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
                markets = exchange.load_markets()
                # output all symbols
                dump(green(id), 'has', len(exchange.symbols), 'symbols:', green(', '.join(exchange.symbols))) 
                delay = int(exchange.rateLimit / 1000)  # delay in between requests
                # fetch ticker
                ticker = exchange.fetch_ticker(self.symbol)
                dump(green(id),
                     green(self.symbol),
                     'ticker',
                     ticker['datetime'],
                     'high: ' + str(ticker['high']),
                     'low: ' + str(ticker['low']),
                     'bid: ' + str(ticker['bid']),
                     'bidVolume: ' + str(ticker['bidVolume']),
                     'ask: ' + str(ticker['ask']),
                     'askVolume: ' + str(ticker['askVolume']),
                     'volume: ' + str(ticker['quoteVolume']))
                
                # don't check balance for speed
                ask_price = ticker['ask']
                bid_price = ticker['bid']
                price = ask_price - (ask_price - bid_price)*0.5
                if price > self.max_buy_price or price < self.min_sell_price:
                    return
                else:
                    # begin duiqiao
                    results = self.duiqiao_async(price)
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
 
    async def create_order(self, price, side):
        try:
            if side == 'sell':
                response = self.instance.create_limit_sell_order(self.symbol, self.base_volume, price)
            elif side == 'buy':
                response = self.instance.create_limit_buy_order(self.symbol, self.base_volume, price)
        except Exception as e:
            print('Failed to create order with', self.instance.id, type(e).__name__, str(e))
            response = None
        return response
 
    @monit_time
    def duiqiao_async(self, price):
        loop = uvloop.new_event_loop()
        asyncio.set_event_loop(loop)
        results = loop.run_until_complete(asyncio.gather(
            self.create_order(price, 'sell'),
            self.create_order(price, 'buy')
            ))     
        return results