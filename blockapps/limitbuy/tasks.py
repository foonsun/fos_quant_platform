# Create your tasks here
from __future__ import absolute_import, unicode_literals
import datetime
from celery import shared_task
from celery.schedules import crontab
from blockserver import celery_app
from .models import LimitbuyPolicy 
from blockuser.models import OPS, RUN_STATUSS
from django.utils import timezone
from time import sleep
from .business import LimitBuy
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from blockdjcom.basebusiness import wslog

@shared_task
def add(x, y):
    print(x,y)
    return x + y 

@celery_app.task
def run_limitbuy_policy(policy_id):
    print(policy_id)
    ws_type = 'limitbuy_message'
    while True:
        policy = LimitbuyPolicy.objects.get(id=policy_id)
        print(policy)
        username = policy.user.username
        exchange = policy.exchange
        symbol = policy.symbol
        accesskey = policy.accesskey
        secretkey = policy.secretkey
        max_buy_price = policy.max_buy_price
        min_sell_price = policy.min_sell_price
        base_volume = policy.base_volume
        start_time = policy.start_time
        end_time = policy.end_time
        update_time = policy.update_time
        create_time = policy.create_time
        status = policy.status
        operation = policy.operation
        limit_price = policy.limit_price
        message = {'policy_id': policy_id, 'data': {'username':username, "exchange": exchange, 'symbol': symbol, 'start_time': start_time.isoformat(), 'end_time': end_time.isoformat()}}
        wslog(username, ws_type, message)
        if operation == OPS[1][0]:
            policy.status = RUN_STATUSS[2][0]
            policy.save()
            break
        elif operation == OPS[0][0]:
            nowtime = timezone.now()
            if policy.start_time > nowtime + datetime.timedelta(microseconds=100):
                sleep(0.5)
                continue
            if policy.end_time < nowtime:
                policy.status = RUN_STATUSS[2][0]
                policy.save()
                break
            #if policy.status == RUN_STATUSS[1][0]:
            #    break
            #else:
            policy.status = RUN_STATUSS[1][0]
            policy.save()
            # 执行限时购买策略开始
            quant = LimitBuy(exchange, symbol, accesskey, secretkey,\
                              max_buy_price, min_sell_price, base_volume, limit_price)    
            ret = quant.run() 
            wslog(username, ws_type, ret)