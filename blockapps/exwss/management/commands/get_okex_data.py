from django.core.management.base import BaseCommand
from exwss.okexws import OkexFutureKlineData, OkexFutureTradeData
from exwss.basedata import *
import logging

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--symbols', nargs='+', type=str, dest='symbols', required=True, \
                help='symbols btc_usdt eth_usdt eos_usdt')

    def handle(self, *args, **options):
        symbols = options['symbols']
        data = OkexFutureKlineData(symbols, 20, None, OKEX_WS_SERVER)
        data.connect()
        data = OkexFutureTradeData(symbols, 20, None, OKEX_WS_SERVER)
        data.connect() 