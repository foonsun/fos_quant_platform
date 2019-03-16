from django.core.management.base import BaseCommand
from blockuser.duiqiao import duiqiao
import logging

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--ex', dest='exchange', required=True, \
                help='exchange')
        parser.add_argument('--pub', dest='publickey', required=True, \
                help='publick key')
        parser.add_argument('--pri', dest='privatekey', required=True, \
                help='private key')
        parser.add_argument('--s', dest='symbol', required=True, \
                help='trade symbol')
        parser.add_argument('--max', dest='max_buy_price', required=True, \
                help='max buy price')
        parser.add_argument('--min', dest='min_sell_price', required=True, \
                help='min sell price')
        parser.add_argument('--v', type=float, dest='base_volume', required=True, \
                help='basevolume to use')

    def handle(self, *args, **options):
        import ipdb;ipdb.set_trace()
        exchange = options['exchange']
        symbol = options['symbol']
        publickey = options['publickey']
        privatekey = options['privatekey']
        base_volume = options['base_volume']
        max_buy_price = options['max_buy_price']
        min_sell_price = options['min_sell_price']
        policy = duiqiao(exchange, symbol, publickey, privatekey, max_buy_price, min_sell_price, base_volume)
        policy.run()