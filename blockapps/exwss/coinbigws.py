from .basews import CoinData
import json
import zlib
from .basedata import Ticker

class CoinbigData(CoinData):
    def _on_open(self, ws):
        print("### opend coinbig")
        #for symbol in self._symbols:
        params = {'datatype': 'ALL', 'data': '28'}
        #params = {'datatype': 'ALL', 'data': '28'}
        request = json.dumps(params)
        print(request)
        ws.send(request)        
    def _on_message(self, ws, message):
        msg = json.loads(zlib.decompress(message))
        if 'datatype' in msg:
            if msg['datatype'] == 'hello':
                print('welcome：', message)
            elif msg['datatype'] == 'REALTIMEDATA':
                print('REALTIMEDATA')
            elif msg['datatype'] == 'KLINEUPDATE':
                print('KLINEUPDATE')
            elif msg['datatype'].startswith('NEW'):
                #print('depth数据：', msg)
                if msg['data']['tradeMappingId'] == '28':
                    symbol = 'ethusdt'
                bid_price = msg['data']['bids'][0]['price']
                bid_volume = msg['data']['bids'][0]['quantity']
                ask_price = msg['data']['asks'][0]['price']
                ask_volume = msg['data']['asks'][0]['quantity']
                last_price = 0
                last_volume = 0
                print(bid_price,bid_volume,ask_price,ask_volume)
                ticker = Ticker(symbol, last_price, last_volume, bid_price, bid_volume, ask_price, ask_volume)

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
            elif msg['datatype'].startswith('DEPTHCHART'):
                if msg['data']['tradeMappingId'] == 28:
                    symbol = 'ethusdt'
                bid_price = msg['data']['bids'][0][0]
                bid_volume = msg['data']['bids'][0][1]
                ask_price = msg['data']['asks'][0][0]
                ask_volume = msg['data']['asks'][0][1]
                last_price = 0
                last_volume = 0
                print('depthchart')
                print(symbol, last_price, last_volume, bid_price,bid_volume,ask_price,ask_volume)
                ticker = Ticker(symbol, last_price, last_volume, bid_price, bid_volume, ask_price, ask_volume)

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
                print(msg)
