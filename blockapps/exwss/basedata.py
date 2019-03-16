from django.conf import settings

# fcoin websocket地址
FCOIN_WS_SERVER = 'wss://api.fcoin.com/v2/ws'
# huobi websocket地址
HUOBI_WS_SERVER = "wss://api.huobi.br.com/ws"
# hbdm websocket地址
HBDM_WS_SERVER = "wss://www.hbdm.com/ws"

#coinbig websocket地址
COINBIG_WS_SERVER = "wss://ws.coinbig.com/ws"
#okex websocket地址
OKEX_WS_SERVER = "wss://real.okex.com:10441/websocket"

Mongo = getattr(settings, 'MONGO', None)

class Ticker(object):
    """
    # 交易对
    symbol = ''
    # 最新成交价
    last_price = 0
    # 最新成交量
    last_volume = 0
    # 买一价
    bid_price = 0
    # 买一量
    bid_volume = 0
    # 卖一价
    ask_price = 0
    # 卖一量
    ask_volume = 0
    """
    def __init__(self, symbol, last_price, last_volume, bid_price, bid_volume, ask_price, ask_volume):
        self.symbol = symbol
        self.last_price = last_price
        self.last_volume = last_volume
        self.bid_price = bid_price
        self.bid_volume = bid_volume
        self.ask_price = ask_price
        self.ask_volume = ask_volume

    def get_symbol(self):
        return self.symbol

    def get_last_price(self):
        return self.last_price

    def get_last_volume(self):
        return self.last_volume

    def get_bid_price(self):
        return self.bid_price

    def get_bid_volume(self):
        return self.bid_volume

    def get_ask_price(self):
        return self.ask_price

    def get_ask_volume(self):
        return self.ask_volume

    def __str__(self):
        s = 'symbol: ' + self.symbol+", last_price: " + str(self.last_price)
        #print(s)
        return s
