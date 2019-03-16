from django.core.management.base import BaseCommand
from oscar.apps.order.models import Order
from oscar.apps.basket.models import Basket
from blockuser.models import QuantPolicyOrder
import logging
from django.utils import timezone

log_sync_orders = logging.getLogger('sync_orders_log')
policy_url_map = {2: ['manage_addduiqiao','manage_getduiqiaolist']}
class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        now = timezone.now()
        orders = Order.objects.filter(date_placed__gte=now-timezone.timedelta(7))
        for order in orders:
            log_sync_orders.info('order:%s' % (order.date_placed))
            date_placed = order.date_placed
            user = order.user
            basket = order.basket
            lines = order.lines
            for line in lines.all():
                product = line.product
                quantity = line.quantity
                policy_id = product.id
                quantorders = QuantPolicyOrder.objects.filter(user=user, policy_id=policy_id)
                for quantorder in quantorders:
                    if quantorder.policy_end_time > date_placed:
                        quantorder.policy_end_time += timezone.timedelta(days=30*quantity)
                    else:
                        quantorder.policy_start_time = date_placed
                        quantorder.policy_end_time = date_placed + timezone.timedelta(days=30*quantity)
                    quantorder.policy_name = line.title
                    quantorder.policy_url_add = policy_url_map[policy_id][0]
                    quantorder.policy_url_list = policy_url_map[policy_id][1]
                    quantorder.save()
                    log_sync_orders.info('quantorder id:%s' %(quantorder.id))
                if not quantorders:
                    policy_end_time = date_placed + timezone.timedelta(days=30*quantity)
                    QuantPolicyOrder.objects.create(user=user, policy_id=policy_id, \
                                                     policy_start_time=date_placed,
                                                     policy_end_time=policy_end_time,
                                                     policy_name=line.title,
                                                     policy_url_add=policy_url_map[policy_id][0],
                                                     policy_url_list=policy_url_map[policy_id][1])   
           
                    log_sync_orders.info('quantorder id:%s' %(quantorder.id))