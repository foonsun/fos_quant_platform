from django.core.management.base import BaseCommand
from exwss.hbdmws import HbdmData
from exwss.basedata import *
import logging

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--symbols', nargs='+', type=str, dest='symbols', required=True, \
                help='symbols BTC_CW BTC_NW BTC_CQ')

    def handle(self, *args, **options):
        symbols = options['symbols']
        data = HbdmData(symbols, 20, None, HBDM_WS_SERVER)
        data.connectSync()