from django.core.management.base import BaseCommand
from fcoin.models import MarketTradeOrderModel
from fcoin.business import Fcoin
import logging

market_trade_log = logging.getLogger('fcoin_market_trade_log') 
class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--symbol', dest='symbol', required=True, help='trade symbol')
        parser.add_argument('--limit', dest='limit', required=True, help='trade limit')
        parser.add_argument('--before', dest='before', required=True, help='before id')

    def handle(self, *args, **options):
        symbol = options['symbol']
        limit = options['limit']
        before = options['before']
        fcoin = Fcoin(0,0)
        result = fcoin.get_market_orders(symbol, limit, before)
        try:
            data = result['data']
            for item in data:
                MarketTradeOrderModel.objects.get_or_create(
                                                    trade_id = item['id'],
                                                    defaults={
                                                        'symbol': symbol,
                                                        'amount': item['amount'],
                                                        'timestamp': item['ts'],
                                                        'side': item['side'],
                                                        'price': item['price']
                                                        })
        except:
            market_trade_log.info(' market trade data key fail')
