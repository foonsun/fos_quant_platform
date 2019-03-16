from django.test import TestCase
from .okexws import OkexFutureKlineData, OkexFutureTradeData
from .basedata import *
import time
from acom.utils.dbutil import connect_mongo
from django.conf import settings

Mongo = getattr(settings, 'MONGO', None)

# Create your tests here.
class MongoTestCase(TestCase):
    def test_connect_mongo(self):
        conn = connect_mongo(Mongo['okex']['host'], Mongo['okex']['port'], Mongo['okex']['username'],\
                       Mongo['okex']['password'], Mongo['okex']['db'])
        item = conn['test'].insert_one({'test': 'test'})
        self.assertTrue(item.inserted_id is not None, 'insert fail')
        item = conn['test'].find_one({'test': 'test'})
        self.assertTrue(item['test'] == 'test', 'can not find')
        item = conn['test'].delete_one({'test': 'test'})
        self.assertTrue(item.deleted_count == 1, 'delete fail')
        item = conn['test'].drop()
        self.assertTrue(item is None, 'delete fail')

class OkexTestCase(TestCase):
    def test_okex_wss_future_kline_data(self):
        data = OkexFutureKlineData(['btc_usdt','eth_usdt','eos_usdt'], 20, None, OKEX_WS_SERVER)
        data.connectSync()
 
    def test_okex_wss_future_trade_data(self):
        data = OkexFutureTradeData(['btc_usdt','eth_usdt','eos_usdt'], 20, None, OKEX_WS_SERVER)
        data.connectSync() 