from django.core import serializers
from .basebusiness import baseFcoin
import json
import logging
import time
from multiprocessing import Process, Pool, Queue
import queue
from blockdjcom.decorators import monit_time 

auto_trade_log = logging.getLogger('fcoin_auto_trade_log') 
class Fcoin(baseFcoin):
    MARKET_DEPTH_LEVEL = 'L20'
    FCOIN_REWARD_REFER = 0.00
    # 查找需要卖的订单
    @monit_time
    def get_orders_to_sell(self, symbol):
        result =[]
        response = self.get_orders_list(symbol, 'filled', '', '', 100)
        if response['status'] != 0:
            return
        orders = response['data']
        if not orders:
            return result
        # 目前只检查最近的2笔订单
        if orders[0]['side'] == 'buy' and orders[0]['state'] in ('filled',\
                'partial_filled', 'partial_canceled'):
                result.append({'symbol': orders[0]['symbol'],
                                'buy_price': orders[0]['price'],
                                'filled_amount': orders[0]['filled_amount'],
                                'buy_order_id': orders[0]['id']
                                })
        return result
    
    # 卖出订单
    @monit_time
    def do_sell_policy(self, symbol, buy_price, remain_amount):
        while True:
            # 查询盘口卖单数量
            level = self.MARKET_DEPTH_LEVEL
            symbol=symbol
            response = self.get_market_depth(symbol, level)
            if response['status'] != 0:
                continue
            depth = response['data']
            buy_1_price = depth['bids'][0]
            buy_1_volume = depth['bids'][1]
            # 目前fcoin盈利规则
            reward_percent = (0.01 + 0.01)*self.FCOIN_REWARD_REFER
            buy_price = buy_price
            # 查询该币种余额，实际买的以余额为准。
            balances = self.get_coin_balances()
            if symbol[-4:] == 'usdt': 
                coin = symbol[:-4]
                available_balance = float(balances[coin]['available'])
            elif symbol[-3:] == 'eth':
                coin = symbol[:-3]
                available_balance = float(balances[coin]['available'])
            elif symbol[-3:] == 'btc':
                coin = symbol[:-3]
                available_balance = float(balances[coin]['available'])
            elif symbol[-2:] == 'ft':
                coin = symbol[:-2]
                available_balance = float(balances[coin]['available'])
            buy_amount = available_balance if available_balance > remain_amount else remain_amount
            if buy_price < buy_1_price * (1 + reward_percent):
                # 立刻卖出
                symbol=symbol
                side='sell'
                order_type='limit'
                sell_price=buy_1_price
                # 
                if buy_amount <= buy_1_volume:
                    sell_amount = buy_amount
                else:
                    sell_amount = buy_1_volume
                response = self.create_order(symbol, side, order_type, str(sell_price), str(sell_amount)) 

                if response['status'] != 0:
                    continue
                sell_order_id = response['data']
                remain_amount = self.check_order_filled_or_not(sell_order_id, sell_amount)
                if remain_amount != 0:
                    continue
                break
    # 查询订单是否成交
    @monit_time
    def check_order_filled_or_not(self, order_id, amount):
        while True:
            remain_amount = 0
            response = self.get_order_by_id(order_id)
            if response['status'] != 0:
                auto_trade_log.info('get order %s  failed: status(%d)' % \
                            (order_id, response['status']))           
                continue 
            if response['data']['state'] == 'filled':
                auto_trade_log.info('side(%s) order_id(%s) filled: filled_amount:%s' %\
                (response['data']['side'], order_id, response['data']['filled_amount']))
                return 0
            elif response['data']['state'] == 'partial_filled':
                remain_amount = amount - response['data']['filled_amount']
                auto_trade_log.info('side(%s) order_id(%s) partial_filled: filled_amount:%s remain_amount:%s ' %\
                (response['data']['side'],order_id, response['data']['filled_amount'], remain_amount))
                return remain_amount
            else:
                auto_trade_log.info('side(%s) order_id(%s) partial_filled: filled_amount:%s remain_amount:%s ' %\
                (response['data']['side'],order_id, response['data']['filled_amount'], amount))
                return amount
        
    # 撤销订单
    @monit_time
    def cancel_order_until_success(self, order_id):
        while True:
            response = self.cancel_order(order_id)
            # 取消失败已经成交的订单 
            if response['status'] != 0:
                auto_trade_log.info('cancel order %s  failed: status(%d)' % \
                                    (order_id, response['status']))           
            return
    # 账户各币种余额
    @monit_time
    def get_coin_balances(self):
        response = self.get_balance()
        if response['status'] != 0:
            auto_trade_log.info('get balance failed: status(%d)' % \
                    (response['status']))           
            return
        rsp_balances = response['data']
        balances = {}
        for balance in rsp_balances:
            balances.update({balance['currency']:{'available':balance['available'],
                                                  'frozen': balance['frozen'],
                                                  'balance': balance['balance']}
                                                  })  
        return balances

    # 下买单
    @monit_time
    def do_buy_policy(self, symbol, percent):
        while True:
            # policy1: 低买高卖策略: buy_price < sell_price * (1 + 0.00004)
            # step1: 获取盘口数据
            depth_queue = Queue()
            p1 = Process(target=fcoin_get_market_depth,args=(self,symbol,depth_queue))
            p1.start()
            p1.join()
            # step2: 下买单
            # 下买单的买入价格如何选取？
            depth = depth_queue.get()
            buy_price = depth[0] 

            # 查询账户余额
            balances = self.get_coin_balances()
            symbol = symbol
            side = 'buy'
            order_type = 'limit'
            buy_price = buy_price
            # 这里可以根据symbol来判断买入的基准货币是哪个
            if symbol[-4:] == 'usdt': 
                available_balance = float(balances['usdt']['available'])
            elif symbol[-3:] == 'eth':
                available_balance = float(balances['eth']['available'])
            elif symbol[-3:] == 'btc':
                available_balance = float(balances['btc']['available'])
            elif symbol[-2:] == 'ft':
                available_balance = float(balances['ft']['available'])
            buy_amount = round(available_balance/buy_price*percent, 4)
            # 下买单
            response = self.create_order(symbol, side, order_type, \
                    str(buy_price), str(buy_amount))
            if response['status'] != 0:
                auto_trade_log.info('buy price:%f amount:%f failed: status(%d)'\
                        %(buy_price, buy_amount, response['status']))           
                continue
            buy_order_id = response['data']
            remain_amount = self.check_order_filled_or_not(buy_order_id, buy_amount)
            if remain_amount == buy_amount:
                self.cancel_order_until_success(buy_order_id)
                continue
            buy_amount = buy_amount - remain_amount
            return buy_price, buy_amount

@monit_time
def fcoin_get_market_depth(fcoin, symbol, depth_result):
    # step3: 获取盘口深度
    level = 'L20'
    response = fcoin.get_market_depth(symbol, level)
    if response['status'] != 0:
        auto_trade_log.info('get %s %s depth failed: status(%d)' % \
                (symbol, level, response['status']))           
    depth = response['data']
    buy_1_price = depth['bids'][0]
    buy_1_volume = depth['bids'][1]
    sell_1_price = depth['asks'][0]
    sell_1_volume = depth['asks'][1]
    depth_result.put([buy_1_price, buy_1_volume, sell_1_price, sell_1_volume])

@monit_time
def fcoin_get_buy_amount(fcoin, symbol, buy_price, percent, buy_queue):
    balances = fcoin.get_coin_balances()
    # 下买单
    symbol = symbol
    side = 'buy'
    order_type = 'limit'
    buy_price = buy_price
    # 这里可以根据symbol来判断买入的基准货币是哪个
    if symbol[-4:] == 'usdt': 
        available_balance = float(balances['usdt']['available'])
    elif symbol[-3:] == 'eth':
        available_balance = float(balances['eth']['available'])
    elif symbol[-3:] == 'btc':
        available_balance = float(balances['btc']['available'])
    elif symbol[-2:] == 'ft':
        available_balance = float(balances['ft']['available'])
    buy_amount = round(available_balance/buy_price*percent, 4)
    buy_queue.put(buy_amount)
