from .basews import CoinData
import json
import gzip
from .basedata import Ticker

class HbdmData(CoinData):
    def _init_(self, symbols, ticker_size, handler, ws_server):
        super()._init_(symbols, ticker_size, handler, ws_server)

    def _on_open(self, ws):
        print("### opened 1 ###")
        for symbol in self._symbols:
            sub = '{"sub": "market.'+symbol+'.depth.step0", \
                    "id": "depth5"}'
            print(sub)
            ws.send(sub)

            sub = '{"sub": "market.' + symbol + '.trade.detail",\
                    "id": "trade"}'
            print(sub)
            ws.send(sub)

    def _on_message(self, ws, message):
        #print(message)
        result=gzip.decompress(message).decode('utf-8')
        if result[:7] == '{"ping"':
            ts=result[8:21]
            pong='{"pong":'+ts+'}'
            ws.send(pong)
        msg = json.loads(result)
        print(msg)
        """
        if 'type' in msg:
            if msg['type'] == 'hello':
                print('welcome：', message)
            elif msg['type'].startswith('ticker'):
                # print('ticker数据：', message)

                symbol = msg['type'][7:]
                last_price = msg['ticker'][0]
                last_volume = msg['ticker'][1]
                bid_price = msg['ticker'][2]
                bid_volume = msg['ticker'][3]
                ask_price = msg['ticker'][4]
                ask_volume = msg['ticker'][5]

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
        """