#encoding=utf8
from blockcomm.context import BaseContext
from django.core.management.base import BaseCommand
from acom.utils.strutil import Object
from django.utils.functional import cached_property

class BlockBaseCommand(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--apikey', dest='apikey', required=False, default='')
        parser.add_argument('--apisecret', dest='apisecret', required=False, default='')

    def handle(self, *args, **options):
        self.args = args
        self.options = options
        self.opts = Object(**options)
        self.work(args, options)

    @cached_property
    def ctx(self):
        return BaseContext(apikey=str(getattr(self.opts, 'apikey', '')),
                           apisecret=str(getattr(self.opts, 'apisecret', '')))
