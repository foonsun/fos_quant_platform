from django.core.management.base import BaseCommand
import logging
import sys,os,traceback
from os.path import join as pathjoin, exists as pathexists
import requests
import json
from django.core.mail import send_mail


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass
    def handle(self, *args, **options):
        api_url = 'https://api.omniexplorer.info/v1/address/addr/details/'
        address = '1C3mL4rhNWukpxtJ4m4DPGo9kf5qeS1dTZ'
        payload = {'addr':address}
        response = requests.post(api_url, data=payload)
        result = json.loads(response.content)
        txs = result['transactions'] 
        if len(txs) == 1:
            message =  '监控地址无转账记录:1C3mL4rhNWukpxtJ4m4DPGo9kf5qeS1dTZ 目前余额 {}'.format(txs[0]['amount']) 
            send_mail(
                     '提醒:监控钱包地址没有转账记录',
                      message,
                     'bearquant@foxmail.com',
                     ['sarah_wang@polysands.com'],
                     fail_silently=False,
                    )
        else:
            message = '1C3mL4rhNWukpxtJ4m4DPGo9kf5qeS1dTZ地址有转账记录，请立刻前往该地址查看：https://www.omniexplorer.info/address/1C3mL4rhNWukpxtJ4m4DPGo9kf5qeS1dTZ' 
            send_mail(
                     '警告：1C3mL4rhNWukpxtJ4m4DPGo9kf5qeS1dTZ地址发生转账',
                      message,
                     'bearquant@foxmail.com',
                     ['andyjoe318@gmail.com', 'sarah_wang@polysands.com'],
                     fail_silently=False,
                    )
