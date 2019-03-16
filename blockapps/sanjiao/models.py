from django.db import models
from blockuser.models import AbstractQuantPolicy
from djcom.admin_perms import PermissionsMixin
from django.core.urlresolvers import reverse

# Create your models here.
class SanjiaoPolicy(AbstractQuantPolicy):
    class Meta(PermissionsMixin.Meta):
        abstract = False
        #app_label = 'quant'
        db_table = 'sanjiao'
        managed = True
        verbose_name = u'三角策略'
    symbol1 = models.CharField(verbose_name='交易对2', max_length=20, default='', help_text='请填写该交易所的交易对例如BTC/USDT')
    symbol2 = models.CharField(verbose_name='交易对3', max_length=20, default='', help_text='请填写该交易所的交易对例如BTC/USDT')
    base_volume = models.FloatField(verbose_name='货币数量', \
                                      help_text='请填写需要赚的币的数量', default=0)
    min_percent = models.FloatField(verbose_name='最小收益百分比',\
                                    help_text='请填写最小套利百分比', default=0)
    def get_absolute_url(self):
        return reverse('manage_getsanjiao', kwargs={'pk': self.pk})