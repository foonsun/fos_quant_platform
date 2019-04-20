from django.core.management.base import BaseCommand
import logging
import sys,os,traceback
from os.path import join as pathjoin, exists as pathexists
import requests
import json
from django.core.mail import send_mail

bet_log = logging.getLogger('betlog') 

class Command(BaseCommand):
    contract_account = 'bobinggame12'
    def add_arguments(self, parser):
        pass
    def handle(self, *args, **options):
        url = 'http://eos.greymass.com/v1/history/get_actions'
        payload = {"account_name": self.contract_account,"pos":-1,"offset":-50}
        response = requests.post(url, data=json.dumps(payload))
        result = json.loads(response.content)
        actions = result['actions'] 
        for action in actions:
            if 'receipt' in action['action_trace'] and 'act' in action['action_trace']:
                if action['action_trace']['act']['account'] == self.contract_account and action['action_trace']['act']['name'] == 'result':
                    one_count = 0
                    two_count = 0
                    three_count = 0
                    four_count = 0
                    five_count = 0
                    six_count = 0
                    result = action['action_trace']['act']['data']['result']
                    random_roll = [result['random_roll_1'], result['random_roll_2'], result['random_roll_3'], result['random_roll_4'],\
                                   result['random_roll_5'], result['random_roll_6']]
                    for roll in random_roll:
                        if roll == 1:
                            one_count += 1
                        elif roll == 2:
                            two_count += 1
                        elif roll == 3:
                            three_count += 1
                        elif roll == 4:
                            four_count += 1
                        elif roll == 5:
                            five_count += 1
                        elif roll == 6:
                            six_count += 1
                    if four_count == 6:
                        bet_log.info("liubeihong occurs! account: %s amount:%s payout: %s randomroll:%d%d%d%d%d%d" % ( result['player'], \
                                                                                                                result['amount'],\
                                                                                                                result['payout'],\
                                                                                                                result['random_roll_1'],\
                                                                                                                result['random_roll_2'],\
                                                                                                                result['random_roll_3'],\
                                                                                                                result['random_roll_4'],\
                                                                                                                result['random_roll_5'], \
                                                                                                                result['random_roll_6'] ))
                        message = '六杯红120倍大奖开出了！账号:%s 下注金额:%s 获得金额:%s 请去浏览器核查该账号交易记录！' % (result['player'],\
                                                                                                                             result['amount'],\
                                                                                                                             result['payout']
                                                                                                                            )
                        send_mail(
                                 '六杯红大奖开出请核查！',
                                 message,
                                 'helloeoswallet@gmail.com',
                                 ['andyjoe318@gmail.com', '55914207@qq.com', 'ym_weng@126.com'],
                                 fail_silently=False,
                                ) 
                    
                    elif six_count == 6 or five_count == 6 or three_count == 6 or two_count == 6:
                        bet_log.info("guandengqiang occurs! account: %s amount:%s payout: %s randomroll:%d%d%d%d%d%d" % ( result['player'], \
                                                                                                                result['amount'],\
                                                                                                                result['payout'],\
                                                                                                                result['random_roll_1'],\
                                                                                                                result['random_roll_2'],\
                                                                                                                result['random_roll_3'],\
                                                                                                                result['random_roll_4'],\
                                                                                                                result['random_roll_5'], \
                                                                                                                result['random_roll_6'] ))
                        message = '关灯枪49倍大奖开出了！账号:%s 下注金额:%s 获得金额:%s 请去浏览器核查该账号交易记录！' % (result['player'],\
                                                                                                                             result['amount'],\
                                                                                                                             result['payout']
                                                                                                                            )
                        send_mail(
                                 '关灯枪大奖开出请核查！',
                                 message,
                                 'helloeoswallet@gmail.com',
                                 ['andyjoe318@gmail.com', '55914207@qq.com', 'ym_weng@126.com'],
                                 fail_silently=False,
                                )
                    elif four_count == 4 and one_count == 2:
                        bet_log.info(" chajinhua occurs! account: %s amount:%s payout: %s randomroll:%d%d%d%d%d%d" % ( result['player'], \
                                                                                                                result['amount'],\
                                                                                                                result['payout'],\
                                                                                                                result['random_roll_1'],\
                                                                                                                result['random_roll_2'],\
                                                                                                                result['random_roll_3'],\
                                                                                                                result['random_roll_4'],\
                                                                                                                result['random_roll_5'], \
                                                                                                                result['random_roll_6'] ))
                        message = '插金花33倍大奖开出了！账号:%s 下注金额:%s 获得金额:%s 请去浏览器核查该账号交易记录！' % (result['player'],\
                                                                                                                             result['amount'],\
                                                                                                                             result['payout']
                                                                                                                            )
                        send_mail(
                                 '插金花大奖开出请核查！',
                                 message,
                                 'helloeoswallet@gmail.com',
                                 ['andyjoe318@gmail.com', '55914207@qq.com', 'ym_weng@126.com'],
                                 fail_silently=False,
                                )
                    elif one_count == 6:
                        bet_log.info("biandijin occurs! account: %s amount:%s payout: %s randomroll:%d%d%d%d%d%d" % ( result['player'], \
                                                                                                                result['amount'],\
                                                                                                                result['payout'],\
                                                                                                                result['random_roll_1'],\
                                                                                                                result['random_roll_2'],\
                                                                                                                result['random_roll_3'],\
                                                                                                                result['random_roll_4'],\
                                                                                                                result['random_roll_5'], \
                                                                                                                result['random_roll_6'] ))
                        message = '遍地锦88倍大奖开出了！账号:%s 下注金额:%s 获得金额:%s 请去浏览器核查该账号交易记录！' % (result['player'],\
                                                                                                                             result['amount'],\
                                                                                                                             result['payout']
                                                                                                                            )
                        send_mail(
                                 '遍地锦大奖开出请核查！',
                                 message,
                                 'helloeoswallet@gmail.com',
                                 ['andyjoe318@gmail.com', '55914207@qq.com', 'ym_weng@126.com'],
                                 fail_silently=False,
                                )

                         
                         
        
