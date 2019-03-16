from .basews import CoinData
import json
import zlib
from .basedata import Ticker, Mongo
from acom.utils.dbutil import connect_mongo
from django.conf import settings
import traceback
import time

class OkexData(CoinData):
    PING_TICK = 0
    PING_INTERVAL = 30
    def _on_open(self, ws):
        print("### opened okex")
        for symbol in self._symbols:
            channel = 'ok_sub_spot_' + symbol + '_ticker'
            params = {'event':'addChannel','channel': channel}
            request = json.dumps(params)
            print(request)
            ws.send(request)
        #ws.send({'event':'ping'})
    
    def _on_message(self, ws, message):
        print(message)
        msg = json.loads(message)

        if msg[0]['channel'].endswith('ticker'):
            symbol = msg[0]['channel'].split('_')[3] + '-' + \
                    msg[0]['channel'].split('_')[5]
            last_price = msg[0]['data']['last']
            last_volume = msg[0]['data']['vol']
            bid_price = msg[0]['data']['buy']
            bid_volume = 0
            ask_price = msg[0]['data']['sell']
            ask_volume = 0

            ticker = Ticker(symbol, last_price, last_volume, bid_price, bid_volume, ask_price, ask_volume)
            print(self._ticker_dict)
            if ticker.get_symbol() in self._ticker_dict:
                ticker_list = self._ticker_dict[ticker.get_symbol()]

                if len(ticker_list) < self._ticker_size:
                    ticker_list.append(ticker)
                else:
                    del ticker_list[0]
                    ticker_list.append(ticker)
            else:
                self._ticker_dict[ticker.get_symbol()] = [ticker]

            self._handler(ticker)
        else:
            print(message)

    def _ping_interval(self, ws):
        nowtime = time.time()
        if self.PING_TICK == 0:
            self.PING_TICK = nowtime
        else:
            if nowtime - self.PING_TICK >= self.PING_INTERVAL:
                self.PING_TICK = nowtime
                ws.send(json.dumps({'event': 'ping'}))

class OkexFutureKlineData(OkexData):
    def _on_open(self, ws):
        print('### opened okex')
        params = []
        for symbol in self._symbols:
            channel_kline = 'ok_sub_futureusd_' + symbol + '_kline_' + 'quarter' + '_1min'
            params.append({'event': 'addChannel', 'channel': channel_kline})
            channel_kline = 'ok_sub_futureusd_' + symbol + '_kline_' + 'next_week' + '_1min'
            params.append({'event': 'addChannel', 'channel': channel_kline})
            channel_kline = 'ok_sub_futureusd_' + symbol + '_kline_' + 'this_week' + '_1min'
            params.append({'event': 'addChannel', 'channel': channel_kline})
        request = json.dumps(params)
        print(request)
        ws.send(request)
        
    def _on_message(self, ws, message):
        self._ping_interval(ws)
        msg = json.loads(message)
        try:
            if msg == {'event': 'pong'}:
                return
            if msg[0]['channel'].startswith('ok_sub_futureusd'):
                conn = connect_mongo(Mongo['okex']['host'], Mongo['okex']['port'], Mongo['okex']['username'],\
                                 Mongo['okex']['password'], Mongo['okex']['db'])
                conn['futurekline'].insert_one(msg[0])
            else:
                print(msg)
        except:
            print(msg)
            traceback.print_exc() 

class OkexFutureTradeData(OkexData):
    def _on_open(self, ws):
        print('### opened okex')
        params = []
        for symbol in self._symbols:
            channel_trade = 'ok_sub_futureusd_' + symbol + '_trade_' + 'quarter'
            params.append({'event': 'addChannel', 'channel': channel_trade})
            channel_trade = 'ok_sub_futureusd_' + symbol + '_trade_' + 'next_week'
            params.append({'event': 'addChannel', 'channel': channel_trade})
            channel_trade = 'ok_sub_futureusd_' + symbol + '_trade_' + 'this_week'
            params.append({'event': 'addChannel', 'channel': channel_trade})
        request = json.dumps(params)
        print(request)
        ws.send(request)
        
    def _on_message(self, ws, message):
        self._ping_interval(ws)
        #print(message) 
        msg = json.loads(message)
        try:
            if msg == {'event': 'pong'}:
                return
            if msg[0]['channel'].startswith('ok_sub_futureusd'):
                conn = connect_mongo(Mongo['okex']['host'], Mongo['okex']['port'], Mongo['okex']['username'],\
                                 Mongo['okex']['password'], Mongo['okex']['db'])
                conn['futuretrade'].insert_one(msg[0])
        except:
            print(msg)
            traceback.print_exc() 