# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from blockserver import celery_app
from .models import SanjiaoPolicy 
from blockuser.models import OPS, RUN_STATUSS
from django.utils import timezone
from time import sleep
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .business import Sanjiao

@celery_app.task
def run_sanjiao_policy(policy_id):
    print(policy_id)
    channel_layer = get_channel_layer()
    while True:
        policy = SanjiaoPolicy.objects.get(id=policy_id)
        print(policy)
        username = policy.user.username
        exchange = policy.exchange
        symbol = policy.symbol
        symbol1 = policy.symbol1
        symbol2 = policy.symbol2
        accesskey = policy.accesskey
        secretkey = policy.secretkey
        min_percent = policy.min_percent
        base_volume = policy.base_volume
        start_time = policy.start_time
        end_time = policy.end_time
        update_time = policy.update_time
        create_time = policy.create_time
        status = policy.status
        operation = policy.operation
        message = {'policy_id': policy_id, 'data': {'username':username, "exchange": exchange, 'symbol': symbol, 'start_time': start_time.isoformat(), 'end_time': end_time.isoformat()}}
        async_to_sync(channel_layer.group_send)(
            username,
            {
                'type': 'sanjiao_message',
                'message': message
            }
            )
        if operation == OPS[1][0]:
            policy.status = RUN_STATUSS[2][0]
            policy.save()
            break
        elif operation == OPS[0][0]:
            nowtime = timezone.now()
            if policy.start_time > nowtime:
                sleep(1)
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
            # 执行单次对敲策略开始
            quant = Sanjiao(exchange, symbol, accesskey, secretkey,\
                              base_volume, symbol1, symbol2, min_percent)    
            quant.run() 