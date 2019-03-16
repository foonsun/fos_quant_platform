#encoding=utf8
from django.db import models
from django.utils import timezone
from djcom.admin_perms import PermissionsMixin
from djcom.utils import dt1970
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from encrypted_fields import EncryptedTextField

EXCHANGES = (
        ('binance', '币安Binance'),
        ('huobipro', '火币Huobi'),
        ('hadax', '火币HADAX'),
        ('okex', 'OKEX'),
        ('bitmex', 'BitMEX'),
        ('bitfinex', 'Bitfinex'),
        ('bitflyer', 'bitFlyer'),
        ('bittrex', 'Bittrex'),
        ('bithumb', 'Bithumb'),
        ('bitmarket', 'bitmarket'),
        ('bitstamp', 'Bitstamp'),
        ('bitz', 'Bit-Z'),
        ('bitlish', 'Bitlish'),
        ('bitsane', 'Bitsane'),
        ('bitso', 'Bitso'),
        ('coinbase', 'coinbase'),
        ('coinex', 'coinex'),
        ('coinexchange', 'coinexchange'),
        ('coinnest', 'coinnest'),
        ('coinone', 'CoinOne'),
        ('cointiger', 'CoinTiger'),
        ('deribit', 'Deribit'),
        ('gateio', 'Gate.io'),
        ('gdax', 'GDAX'),
        ('hitbtc2', 'HitBTC'),
        ('fcoin', 'FCoin'),
        ('bcex', 'BCEX'),
        ('bibox', 'Bibox'),
        ('bigone', 'BigONE'),
        ('bitbank', 'bitbank'),
        ('bitbay', 'BitBay'),
        ('kraken', 'Kraken'),
        ('kucoin', 'Kucoin'),
        ('lbank', 'LBank'),
        ('poloniex', 'Poloniex'),
        ('qryptos', 'QRYPTOS'),
        ('quoinex', 'QUOINEX'),
        ('tidebit', 'TideBit'),
        ('uex', 'UEX'),
        ('vbtc', 'VTBC'),
        ('wex', 'WEX'),
        ('zb', 'ZB'),
        ('yobit', 'YoBit'),
        ('zaif', 'Zaif'),
    )
SYMBOLS = (
        ('BTC/USDT', 'BTC/USDT'),
        ('ETH/USDT', 'ETH/USDT'),
    )
RUN_STATUSS = (
        ('unstart', '未开始'),
        ('run', '运行中'),
        ('stop', '已停止'),
    )
OPS = (
    (0, '开启运行'),
    (1, '停止运行'),
    )
class QuantPolicy(PermissionsMixin):
    class Meta(PermissionsMixin.Meta):
        abstract = False
        #app_label = 'quant'
        db_table = 'quant_policy'
        managed = True
        verbose_name = u'quant_policy'
 
    title = models.CharField(max_length=255, verbose_name='商品名称', default='')
    price = models.FloatField(verbose_name='购买价格', default=0)
    content = models.TextField(verbose_name='内容', default='')
    exchanges = models.TextField(verbose_name='支持交易所列表', default='')
    #symbols = models.IntegerField(verbose_name='支持交易对', default=0)
    status = models.IntegerField(verbose_name='状态', default=0)
    update_time = models.DateTimeField(verbose_name='记录更新时间', auto_now=True)
    create_time = models.DateTimeField(verbose_name='记录创建时间', auto_now_add=True)
    
    def __str__(self):
        return 'title(%s) price(%s) exchange(%s) ' % \
                           (self.title, self.price, self.exchanges)

class QuantPolicyOrder(PermissionsMixin):
    class Meta(PermissionsMixin.Meta):
        abstract = False
        #app_label = 'quant'
        db_table = 'quant_policy_order'
        managed = True
        verbose_name = u'quant_policy_order'
    
    user = models.ForeignKey(
        User, null=True, blank=True,
        verbose_name=_("User"), on_delete=models.CASCADE)
    policy_id = models.CharField(max_length=20)
    policy_start_time = models.DateTimeField()
    policy_end_time = models.DateTimeField()
    date_created = models.DateTimeField(_("Date Created"), auto_now_add=True)
    date_updated = models.DateTimeField(_("Date Updated"), auto_now=True)
    policy_name = models.CharField(max_length=200, default='')
    policy_url_add = models.CharField(max_length=50, default='')
    policy_url_list = models.CharField(max_length=50, default='')
 
    def __str__(self):
        return 'user %s' % (self.user)

class AbstractQuantPolicy(PermissionsMixin):
    class Meta(PermissionsMixin.Meta):
        abstract = True

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exchange = models.CharField(verbose_name='交易所', max_length=20, choices=EXCHANGES, help_text='请选择一个交易所')
    accesskey = models.CharField(verbose_name='Accesskey', max_length=100, help_text='请填写您在交易所的api access key')
    secretkey = EncryptedTextField(verbose_name='SecretKey', help_text='请填写您在交易所的api secret key')
    symbol = models.CharField(verbose_name='交易对', max_length=20, default='', help_text='请填写该交易所的交易对例如BTC/USDT')
    max_buy_price = models.FloatField(verbose_name='最高买入价格', default=0, \
                                        help_text='请填写该交易对的最高买入价格')
    min_sell_price = models.FloatField(verbose_name='最低卖出价格', default=0, \
                                         help_text='请填写该交易对的最低卖出价格')
    start_time = models.DateTimeField(verbose_name='开始运行时间', help_text='请填写您的交易策略运行开始时间')
    end_time = models.DateTimeField(verbose_name='结束运行时间', help_text='请填写您的交易策略结束运行时间')
    update_time = models.DateTimeField(verbose_name='记录更新时间', auto_now=True)
    create_time = models.DateTimeField(verbose_name='记录创建时间', auto_now_add=True)
    status = models.CharField(verbose_name='运行状态', default='unstart', choices=RUN_STATUSS, blank=True, \
                              max_length=10, help_text='策略运行状态')
    operation = models.IntegerField(verbose_name='操作', default=0, choices=OPS,blank=True,\
                                    help_text='操作')
                
    def __str__(self):
        return 'user(%s) exchange(%s) symbol(%s) start_time(%s) end_time(%s)' % \
            (self.user, self.exchange, self.symbol, self.start_time, self.end_time)