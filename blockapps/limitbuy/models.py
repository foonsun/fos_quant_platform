from django.db import models
from blockuser.models import AbstractQuantPolicy
from djcom.admin_perms import PermissionsMixin
from django.core.urlresolvers import reverse

# Create your models here.
class LimitbuyPolicy(AbstractQuantPolicy):
    class Meta(PermissionsMixin.Meta):
        abstract = False
        #app_label = 'quant'
        db_table = 'limitbuy'
        managed = True
        verbose_name = u'限时抢购策略'
    base_volume = models.FloatField(verbose_name='base货币数量', \
                                      help_text='请填写交易对的币数量比如BTC/USDT就是BTC的数量', default=0)  
    limit_price = models.FloatField(verbose_name='限价买单价格', default=0, \
                                         help_text='请填写该交易对的限价买单价格')
    def get_absolute_url(self):
        return reverse('manage_getlimitbuy', kwargs={'pk': self.pk})