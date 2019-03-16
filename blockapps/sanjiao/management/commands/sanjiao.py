from django.core.management.base import BaseCommand
from sanjiao.business import Sanjiao
import logging

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--ex', dest='exchange', required=True, \
                help='exchange')
        parser.add_argument('--pub', dest='publickey', required=True, \
                help='public key')
        parser.add_argument('--pri', dest='privatekey', required=True, \
                help='private key')
        parser.add_argument('--symbols', nargs='+', type=str, dest='symbols', required=True, \
                help='trade symbol,such as btc/usdt,eth/btc,eth/usdt')
        parser.add_argument('--v', type=float, dest='base_volume', required=True, \
                help='basevolume to use')
        parser.add_argument('--percent', type=float, dest='min_percent', required=True, \
                help='basevolume to use')

    def handle(self, *args, **options):
        exchange = options['exchange']
        symbols = options['symbols']
        publickey = options['publickey']
        privatekey = options['privatekey']
        base_volume = options['base_volume']
        min_percent = options['min_percent']
        policy = Sanjiao(exchange, symbols[0], publickey, privatekey, base_volume, symbols[1], symbols[2], min_percent)
        while True:
            policy.run()