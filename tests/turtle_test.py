
"""
Requires Catalyst version 0.3.0 or abovep
u
q
Tested on Catalyst version 0.3.3
This example aims to provide an easy way for users to learn how to
collect data from any given exchange and select a subset of the available currency pairs for trading. You simply need to specify the exchange and
the market (base_currency) that you want to focus on. You will then see
how to create a universe of assets, and filter it based the market you
desire.
The example prints out the closing price of all the pairs for a given
market in a given exchange every 30 minutes. The example also contains
the OHLCV data with minute-resolution for the past seven days which
could be used to create indicators. Use this code as the backbone to
create your own trading strategy.
The lookback_date variable is used to ensure data for a coin existed on
the lookback period specified.
To run, execute the following two commands in a terminal (inside catalyst
environment). The first one retrieves all the pricing data needed for this
script to run (only needs to be run once), and the second one executes this
script with the parameters specified in the run_algorithm() call at the end
of the file:
catalyst ingest-exchange -x bitfinex -f minute
python turtle.py
"""
from datetime import timedelta

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import talib

from catalyst import run_algorithm
from catalyst.api import (record, symbols, order, order_target, order_target_percent)
from catalyst.exchange.utils.exchange_utils import get_exchange_symbols
from catalyst.exchange.utils.stats_utils import extract_transactions


def initialize(context):    
    context.i = -1  # minute counter
    context.exchange = list(context.exchanges.values())[0].name.lower()
    context.base_currency = list(context.exchanges.values())[
        0].quote_currency.lower()
    context.base_price = None
    context.openTriggers = {
        'fastL': 0,
        'fastS': 0,
        'slowL': 0,
        'slowS': 0
    }
    context.openPrices = {
        'fastL': [],
        'fastS': [],
        'slowL': [],
        'slowS': []
    }
    context.earn = {
        'fastL': [],
        'fastS': [],
        'slowL': [],
        'slowS': []
    }
    context.closeFlag = {
        'fastL': False,
        'fastS': False,
        'slowL': False,
        'slowS': False
    }
    context.openCount = 0
    context.closeCount  = {
        'fastL': 0,
        'fastS': 0,
        'slowL': 0,
        'slowS': 0
        
    }
    context.openPrice = []
    context.copycontent = [] 

def handle_data1(context, data):
    context.i += 1
    lookback_days = 10  # 7 days

    # current date & time in each iteration formatted into a string
    now = data.current_dt
    date, time = now.strftime('%Y-%m-%d %H:%M:%S').split(' ')
    lookback_date = now - timedelta(days=lookback_days)
    # keep only the date as a string, discard the time
    lookback_date = lookback_date.strftime('%Y-%m-%d %H:%M:%S').split(' ')[0]

    one_day_in_minutes = 1440  # 60 * 24 assumes data_frequency='minute'
    # update universe everyday at midnight
    if not context.i % one_day_in_minutes:
        context.universe = universe(context, lookback_date, date)

    # get data every 30 minutes
    minutes = 120  

    # get lookback_days of history data: that is 'lookback' number of bins
    lookback = int(one_day_in_minutes / minutes * lookback_days)
    if not context.i % minutes and context.universe:
        # we iterate for every pair in the current universe
        for coin in context.coins:
            pair = str(coin.symbol)
            if pair == 'btc_usd':
                context.coin = coin
                # Get 30 minute interval OHLCV data. This is the standard data
                # required for candlestick or indicators/signals. Return Pandas
                # DataFrames. 30T means 30-minute re-sampling of one minute data.
                # Adjust it to your desired time interval as needed.
                opened = fill(data.history(coin,
                                        'open',
                                        bar_count=lookback,
                                        frequency='2H')).values
               # import ipdb;ipdb.set_trace()
                high = fill(data.history(coin,
                                        'high',
                                        bar_count=lookback,
                                        frequency='2H')).values
                low = fill(data.history(coin,
                                        'low',
                                        bar_count=lookback,
                                        frequency='2H')).values
                close = fill(data.history(coin,
                                        'price',
                                        bar_count=lookback,
                                        frequency='2H')).values
                volume = fill(data.history(coin,
                                        'volume',
                                        bar_count=lookback,
                                        frequency='2H')).values

                # close[-1] is the last value in the set, which is the equivalent
                # to current price (as in the most recent value)
                # displays the minute price for each pair every 30 minutes
                print('{now}: {pair} -\tO:{o},\tH:{h},\tL:{c},\tC{c},'
                    '\tV:{v}'.format(
                        now=now,
                        pair=pair,
                        o=opened[-1],
                        h=high[-1],
                        l=low[-1],
                        c=close[-1],
                        v=volume[-1],
                    ))
                
                current = lookback
                enter_fast = current -55
                exit_fast = current - 20
                enter_slow = current - 32
                exit_slow = current - 16
                fastL = max(high[enter_fast:current-1])
                fastLC = min(low[exit_fast:current-1])
                fastS = min(low[enter_fast:current-1])
                fastSC = max(high[exit_fast:current-1])

                slowL = max(high[enter_slow:current-1])
                slowLC = min(low[exit_slow:current-1])
                slowS = min(low[enter_slow:current-1])
                slowSC = max(high[exit_slow:current-1])
                
                # cal 波幅
                tech = talib.ATR(high, low, close, 20)  
                
                # 买入点和卖出点
                
                # TODO: Try to add risk limits!
                enterL1 = high[-1] > fastL
                exitL1 = low[-1] <= fastLC
                enterS1 = low[-1] < fastS
                exitS1 = high[-1] >= fastSC

                enterL2 = high[-1] > slowL
                exitL2 = low[-1] <= slowLC
                enterS2 = low[-1] < slowS
                exitS2 = high[-1] >= slowSC

                
               
               
                # Since we are using limit orders, some orders may not execute immediately
                # we wait until all orders are executed before considering more trades.
                orders = context.blotter.open_orders
                if len(orders) > 0:
                    return
                position = context.portfolio.positions[coin].amount
                print(enterL1,context.openTriggers)
                global earn
                pnl_thistime=0
                if context.closeFlag['fastL'] == True:
                    pnl = context.portfolio.pnl
                    #global earn
                    pnl_thistime = pnl - sum(earn['fastL'])
                    earn['fastL'].append(pnl_thistime)
                    context.closeFlag['fastL'] = False 
                if context.closeFlag['fastS'] == True:
                    pnl = context.portfolio.pnl
                    #global earn
                    pnl_thistime = pnl - sum(earn['fastS'])
                    earn['fastS'].append(pnl_thistime)
                    context.closeFlag['fastS'] = False 
                # strategy.entry("fast L", strategy.long, when = (enterL1 and (time > timestamp(FromYear, FromMonth, FromDay, 00, 00)) and (time < timestamp(ToYear, ToMonth, ToDay, 23, 59))))
                # strategy.entry("fast L", strategy.long, when = (enterL1 and (time > timestamp(FromYear, FromMonth, FromDay, 00, 00)) and (time < timestamp(ToYear, ToMonth, ToDay, 23, 59))))
                
                if position and len(context.openPrices['fastL']) and context.openPrices['fastL'][-1] -close[-1]> 2*tech[-1]:
                    print('stop loss for long')
                    order_target_percent(coin, 0)
                    context.openTriggers['fastL'] = 0
                    context.openPrices['fastL'] = []
                    context.closeFlag['fastL'] = True 
# pnl_last=context.portfolio.pnl
            
                if position and len(context.openPrices['fastS']) and context.openPrices['fastS'][-1] -close[-1]<- 2*tech[-1]:
                    print('stop loss for short')
                    order_target_percent(coin, 0)
                    context.openTriggers['fastS'] = 0
                    context.openPrices['fastS'] = []
                    context.closeFlag['fastS'] = True
                # strategy.close("fast L", when = (exitL1 and (time < timestamp(ToYear, ToMonth, ToDay, 23, 59))))
                # Check holdings, if long, then flatten, otherwise, do nothing
            
                if exitL1 and context.openTriggers['fastL']!=0:
                    print("Close Long")
                    order_target_percent(coin, 0)
                    context.openTriggers['fastL'] = 0
                    context.openPrices['fastL'] = []
                    context.closeFlag['fastL'] = True
                          
                # strategy.close("fast S", when = (exitS1 and (time < timestamp(ToYear, ToMonth, ToDay, 23, 59))))
                # Check holdings, if short, then flatten, otherwise, do nothing
                if exitS1 and context.openTriggers['fastS']!=0:
                    print("Close Short")
                    order_target_percent(coin, 0)
                    context.openTriggers['fastS'] = 0
                    context.openPrices['fastS']=[]
                    context.closeFlag['fastS']=True
               
                 
                if context.openTriggers['fastL'] < 4 and len(context.openPrices['fastS']) == 0:
                    if len(context.openPrices['fastL']) and close[-1]>context.openPrices['fastL'][-1]:
                        print('Reloading  Long')
                        fastL = context.openPrices['fastL'][-1] + tech[-1]*0.5
#       import ipdb;ipdb.set_trace()
                        pos_amount = context.portfolio.portfolio_value
                        volume = pos_amount * 0.01 / tech[-1]
                        orderid = order(coin, amount=volume)
                    #order_target_percent(coin, 0.01)
                        context.openTriggers['fastL'] += 1
                        print("fastL",context.openTriggers['fastL'])
                        context.openPrices['fastL'].append(fastL)
                    elif enterL1 and len(context.openPrices['fastL'])==0:
                       # import ipdb;ipdb.set_trace()
                        context.openPrices['fastL'].append(fastL)
                        fastL = fastL + tech[-1]*0.5
                        pos_amount = context.portfolio.portfolio_value
                        volume = pos_amount * 0.01 / tech[-1]
                        orderid = order(coin, amount=volume)
                        #order_target_percent(coin, 0.01)
                        context.openTriggers['fastL'] += 1
                        print("fastL",context.openTriggers['fastL'])
                        context.openPrices['fastL'].append(fastL)
                # strategy.entry("fast S", strategy.short, when = (enterS1 and (time > timestamp(FromYear, FromMonth, FromDay, 00, 00)) and (time < timestamp(ToYear, ToMonth, ToDay, 23, 59))))
                
                if  context.openTriggers['fastS'] < 4 and len(context.openPrices['fastL']) == 0:
                    if len(context.openPrices['fastS']) and close[-1]<context.openPrices['fastS'][-1]:
                        print("reloading short")
                        fastS =context.openPrices['fastS'][-1] - tech[-1]*0.5
                        pos_amount = context.portfolio.portfolio_value
                        volume = pos_amount * 0.01 / tech[-1]
                        orderid = order(coin, amount=-volume)
                    #order_target_percent(coin, 0.01)
                        context.openTriggers['fastS'] += 1
                        context.openPrices['fastS'].append(fastS)
                    elif enterS1 and len(context.openPrices['fastS'])==0:
                       # import ipdb;ipdb.set_trace()
                        print('open short')
                        context.openPrices['fastS'].append(fastS)
                        fastS = fastS - tech[-1]*0.5
                        pos_amount = context.portfolio.portfolio_value
                        volume = pos_amount * 0.01 / tech[-1]
                        orderid = order(coin, amount=-volume)
                        #order_target_percent(coin, 0.01)
                        context.openTriggers['fastS'] += 1
                        context.openPrices['fastS'].append(fastS)
                  
                
                

                
                
                '''
                # strategy.entry("slow L", strategy.long, when = (enterL2 and (time > timestamp(FromYear, FromMonth, FromDay, 00, 00)) and (time < timestamp(ToYear, ToMonth, ToDay, 23, 59))))
                if enterL2 and not context.openTriggers['slowL']:
                    print("Open slow Long")
                    order_target_percent(coin, 0.05)
                    context.openTriggers['slowL'] = True

                # strategy.entry("slow S", strategy.short, when = (enterS2 and (time > timestamp(FromYear, FromMonth, FromDay, 00, 00)) and (time < timestamp(ToYear, ToMonth, ToDay, 23, 59))))
                if enterS2 and not context.openTriggers['slowS']:
                    print("Open slow Short")
                    order_target_percent(coin, -0.05)
                    context.openTriggers['slowS'] = True

                # strategy.close("slow L", when = (exitL2 and (time < timestamp(ToYear, ToMonth, ToDay, 23, 59))))
                if exitL2 and position > 0 and context.openTriggers['slowL']:
                    print("Close slow Long")
                    order_target_percent(coin, 0)
                    context.openTriggers['slowL'] = False

                # strategy.close("slow S", when = (exitS2 and (time < timestamp(ToYear, ToMonth, ToDay, 23, 59))))
                if exitS2 and position < 0 and context.openTriggers['slowS']:
                    print("Close slow Short")
                    order_target_percent(coin, 0)
                    context.openTriggers['slowS'] = False
                '''
                # // zl=0
                # // z=strategy.netprofit / 37 * koef  //ежемесячная прибыль
                # // z=strategy.grossprofit/strategy.grossloss
                # // z1=plot (z, style=line, linewidth=3, color = z>zl?green:red, transp = 30)
                # // hline(zl, title="Zero", linewidth=1, color=gray, linestyle=dashed)
                # // plot(strategy.equity)
                # Let's keep the price of our asset in a more handy variable
                price = data.current(coin, 'price')

                # If base_price is not set, we use the current value. This is the
                # price at the first bar which we reference to calculate price_change.
                if context.base_price is None:
                    context.base_price = price
                price_change = (price - context.base_price) / context.base_price

                record(price=price,
                       cash=context.portfolio.cash,
                       price_change=price_change,
                       fastL=fastL,
                       fastLC=fastLC,
                       fastS=fastS,
                       fastSC=fastSC,
                       slowL=slowL,
                       lowLC=slowLC,
                       slowS=slowS,
                       slowSC=slowSC,
                       pnl=pnl_thistime     
                       )

def handle_data(context, data):
    context.i += 1
    lookback_days = 7  # 7 days

    # current date & time in each iteration formatted into a string
    now = data.current_dt
    date, time = now.strftime('%Y-%m-%d %H:%M:%S').split(' ')
    lookback_date = now - timedelta(days=lookback_days)
    # keep only the date as a string, discard the time
    lookback_date = lookback_date.strftime('%Y-%m-%d %H:%M:%S').split(' ')[0]

    one_day_in_minutes = 1440  # 60 * 24 assumes data_frequency='minute'
    # update universe everyday at midnight
    if not context.i % one_day_in_minutes:
        context.universe = universe(context, lookback_date, date)

    # get data every 30 minutes
    minutes = 240  

    # get lookback_days of history data: that is 'lookback' number of bins
    lookback = int(one_day_in_minutes / minutes * lookback_days)
    if not context.i % minutes and context.universe:
        # we iterate for every pair in the current universe
        for coin in context.coins:
            pair = str(coin.symbol)
            if pair == 'btc_usd':
                context.coin = coin
                # Get 30 minute interval OHLCV data. This is the standard data
                # required for candlestick or indicators/signals. Return Pandas
                # DataFrames. 30T means 30-minute re-sampling of one minute data.
                # Adjust it to your desired time interval as needed.
                opened = fill(data.history(coin,
                                        'open',
                                        bar_count=lookback,
                                        frequency='4H')).values
                #import ipdb;ipdb.set_trace()
                high = fill(data.history(coin,
                                        'high',
                                        bar_count=lookback,
                                        frequency='4H')).values
                low = fill(data.history(coin,
                                        'low',
                                        bar_count=lookback,
                                        frequency='4H')).values
                close = fill(data.history(coin,
                                        'price',
                                        bar_count=lookback,
                                        frequency='4H')).values
                volume = fill(data.history(coin,
                                        'volume',
                                        bar_count=lookback,
                                        frequency='4H')).values

                # close[-1] is the last value in the set, which is the equivalent
                # to current price (as in the most recent value)
                # displays the minute price for each pair every 30 minutes
                print('{now}: {pair} -\tO:{o},\tH:{h},\tL:{c},\tC{c},'
                    '\tV:{v}'.format(
                        now=now,
                        pair=pair,
                        o=opened[-1],
                        h=high[-1],
                        l=low[-1],
                        c=close[-1],
                        v=volume[-1],
                    ))
                    
                current = lookback
                enter_fast = current - 20
                exit_fast = current - 10
                enter_slow = current - 32
                exit_slow = current - 16
                fastL = max(high[enter_fast:current-1])
                fastLC = min(low[exit_fast:current-1])
                fastS = min(low[enter_fast:current-1])
                fastSC = max(high[exit_fast:current-1])

                slowL = max(high[enter_slow:current-1])
                slowLC = min(low[exit_slow:current-1])
                slowS = min(low[enter_slow:current-1])
                slowSC = max(high[exit_slow:current-1])
                
                # cal 波幅
                tech = talib.ATR(high, low, close, 20)  
                
                # 买入点和卖出点
                
                # TODO: Try to add risk limits!
                enterL1 = high[-1] > fastL
                exitL1 = low[-1] <= fastLC
                enterS1 = low[-1] < fastS
                exitS1 = high[-1] >= fastSC

                enterL2 = high[-1] > slowL
                exitL2 = low[-1] <= slowLC
                enterS2 = low[-1] < slowS
                exitS2 = high[-1] >= slowSC

                # Since we are using limit orders, some orders may not execute immediately
                # we wait until all orders are executed before considering more trades.
                orders = context.blotter.open_orders
                if len(orders) > 0:
                    return
                position = context.portfolio.positions[coin].amount
                print(enterL1,context.openTriggers)

                if context.closeFlag['fastL'] == True:
                    pnl = context.portfolio.pnl
                    context.closeFlag['fastL'] = False 
                    context.closeCount['fastL'] += 1
                # strategy.entry("fast L", strategy.long, when = (enterL1 and (time > timestamp(FromYear, FromMonth, FromDay, 00, 00)) and (time < timestamp(ToYear, ToMonth, ToDay, 23, 59))))
                if position and context.openPrices['fastL'][-1] -close[-1]> 2*tech[-1]:
                    print('stop loss')
                    order_target_percent(coin, 0)
                    context.openTriggers['fastL'] = 0
                    context.openPrices['fastL'] = []
                    context.closeFlag['fastL'] = True 
                    context.closeCount['fastL'] += 1 
# pnl_last=context.portfolio.pnl

                if enterL1 and context.openTriggers['fastL'] < 4:
                    print("Open Long")
                    index = context.closeCount['fastL']
                    global earn
                    if index > 0 and earn['fastL'][index-1] > 0:
                        context.closeCount['fastL'] += 1
                        return
                    if len(context.openPrices['fastL']) and fastL > context.openPrices['fastL'][-1]:
                        fastL = context.openPrices['fastL'][-1] + tech[-1]*0.5
#       import ipdb;ipdb.set_trace()
                    
                    pos_amount = context.portfolio.portfolio_value
                    volume = pos_amount * 0.01 / tech[-1]
                    orderid = order(coin, amount=volume)
                    #order_target_percent(coin, 0.01)
                    context.openTriggers['fastL'] += 1
                    print("fastL",context.openTriggers['fastL'])
                    context.openPrices['fastL'].append(fastL)

                '''
                # strategy.entry("fast S", strategy.short, when = (enterS1 and (time > timestamp(FromYear, FromMonth, FromDay, 00, 00)) and (time < timestamp(ToYear, ToMonth, ToDay, 23, 59))))
                if enterS1 and not context.openTriggers['fastS'] < 4:
                    print("Open Short")
                    if len(context.openPrices['fastS']) and fastS > context.openPrices['fastS'][-1]:
                        fastS = context.openPrices['fastS'][-1]+ tech[-1]*0.5
                    pos_amount = context.portfolio.cash
                    volume = pos_amount * 0.01 / tech[-1]
                    orderid = order(coin, amount=volume)
                    #order_target_percent(coin, 0.01)
                    context.openTriggers['fastS'] += 1
                    context.openPrices['fastS'].append(fastS)
                '''
                
                # strategy.close("fast L", when = (exitL1 and (time < timestamp(ToYear, ToMonth, ToDay, 23, 59))))
                # Check holdings, if long, then flatten, otherwise, do nothing
                if exitL1 and position > 0 and context.openTriggers['fastL']:
                    print("Close Long")
                    order_target_percent(coin, 0)
                    context.openTriggers['fastL'] = 0
                    context.openPrices['fastL'] = []
                    context.closeFlag['fastL'] = True
                    context.closeCount['fastL'] += 1
                    '''
                    if (pnl_last- context.portfolio.pnl) > 0:
                        context.earnFlag['fastL'] = True
                    ''' 

                '''
                # strategy.close("fast S", when = (exitS1 and (time < timestamp(ToYear, ToMonth, ToDay, 23, 59))))
                # Check holdings, if short, then flatten, otherwise, do nothing
                if exitS1 and position < 0 and context.openTriggers['fastS']:
                    print("Close Short")
                    order_target_percent(coin, 0)
                    context.openTriggers['fastS'] = 0
            
                '''
                '''
                # strategy.entry("slow L", strategy.long, when = (enterL2 and (time > timestamp(FromYear, FromMonth, FromDay, 00, 00)) and (time < timestamp(ToYear, ToMonth, ToDay, 23, 59))))
                if enterL2 and not context.openTriggers['slowL']:
                    print("Open slow Long")
                    order_target_percent(coin, 0.05)
                    context.openTriggers['slowL'] = True

                # strategy.entry("slow S", strategy.short, when = (enterS2 and (time > timestamp(FromYear, FromMonth, FromDay, 00, 00)) and (time < timestamp(ToYear, ToMonth, ToDay, 23, 59))))
                if enterS2 and not context.openTriggers['slowS']:
                    print("Open slow Short")
                    order_target_percent(coin, -0.05)
                    context.openTriggers['slowS'] = True

                # strategy.close("slow L", when = (exitL2 and (time < timestamp(ToYear, ToMonth, ToDay, 23, 59))))
                if exitL2 and position > 0 and context.openTriggers['slowL']:
                    print("Close slow Long")
                    order_target_percent(coin, 0)
                    context.openTriggers['slowL'] = False

                # strategy.close("slow S", when = (exitS2 and (time < timestamp(ToYear, ToMonth, ToDay, 23, 59))))
                if exitS2 and position < 0 and context.openTriggers['slowS']:
                    print("Close slow Short")
                    order_target_percent(coin, 0)
                    context.openTriggers['slowS'] = False
                '''
                # // zl=0
                # // z=strategy.netprofit / 37 * koef  //ежемесячная прибыль
                # // z=strategy.grossprofit/strategy.grossloss
                # // z1=plot (z, style=line, linewidth=3, color = z>zl?green:red, transp = 30)
                # // hline(zl, title="Zero", linewidth=1, color=gray, linestyle=dashed)
                # // plot(strategy.equity)
                # Let's keep the price of our asset in a more handy variable
                price = data.current(coin, 'price')

                # If base_price is not set, we use the current value. This is the
                # price at the first bar which we reference to calculate price_change.
                if context.base_price is None:
                    context.base_price = price
                price_change = (price - context.base_price) / context.base_price

                record(price=price,
                       cash=context.portfolio.cash,
                       price_change=price_change,
                       fastL=fastL,
                       fastLC=fastLC,
                       fastS=fastS,
                       fastSC=fastSC,
                       slowL=slowL,
                       slowLC=slowLC,
                       slowS=slowS,
                       slowSC=slowSC)


def analyze(context, perf):
    # Get the base_currency that was passed as a parameter to the simulation
    exchange = list(context.exchanges.values())[0]
    base_currency = exchange.quote_currency.upper()
    plt.figure(figsize=(10,10))
   
# First chart: Plot portfolio value using base_currency
    ax1 = plt.subplot(411)
    perf.loc[:, ['portfolio_value']].plot(ax=ax1)
    ax1.legend_.remove()
    ax1.set_ylabel('Portfolio Value\n({})'.format(base_currency))
    start, end = ax1.get_ylim()
    ax1.yaxis.set_ticks(np.arange(start, end, (end - start) / 5))

    # Second chart: Plot asset price, moving averages and buys/sells
    ax2 = plt.subplot(412, sharex=ax1)
    perf.loc[:, ['price', 'fastL', 'fastLC']].plot(
        ax=ax2,
        label='Price')
    ax2.legend_.remove()
    ax2.set_ylabel('{asset}\n({base})'.format(
        asset=context.coin.symbol,
        base=base_currency
    ))
    start, end = ax2.get_ylim()
    ax2.yaxis.set_ticks(np.arange(start, end, (end - start) / 5))

    transaction_df = extract_transactions(perf)
    if not transaction_df.empty:
        buy_df = transaction_df[transaction_df['amount'] > 0]
        sell_df = transaction_df[transaction_df['amount'] < 0]
        ax2.scatter(
            buy_df.index.to_pydatetime(),
            perf.loc[buy_df.index, 'price'],
            marker='^',
            s=50,
            c='green',
            label=''
        )
        ax2.scatter(
            sell_df.index.to_pydatetime(),
            perf.loc[sell_df.index, 'price'],
            marker='v',
            s=50,
            c='red',
            label=''
        )

    # Third chart: Compare percentage change between our portfolio
    # and the price of the asset
    ax3 = plt.subplot(413, sharex=ax1)
    perf.loc[:, ['algorithm_period_return']].plot(ax=ax3)
    ax3.legend_.remove()
    ax3.set_ylabel('Percent Change')
    start, end = ax3.get_ylim()
    ax3.yaxis.set_ticks(np.arange(start, end, (end - start) / 5))

    # Fourth chart: Plot our cash
    ax4 = plt.subplot(414, sharex=ax1)
    perf.cash.plot(ax=ax4)
    ax4.set_ylabel('Cash\n({})'.format(base_currency))
    start, end = ax4.get_ylim()
    ax4.yaxis.set_ticks(np.arange(0, end, end / 5))

    plt.show()
    plt.savefig('table.png')
    
    #Fifth chart
    

    #Sharpe Ratio




# Get the universe for a given exchange and a given base_currency market
# Example: Poloniex BTC Market
def universe(context, lookback_date, current_date):
    # get all the pairs for the given exchange
    json_symbols = get_exchange_symbols(context.exchange)
    # convert into a DataFrame for easier processing
    df = pd.DataFrame.from_dict(json_symbols).transpose().astype(str)
    df['base_currency'] = df.apply(lambda row: row.symbol.split('_')[1],
                                   axis=1)
    df['market_currency'] = df.apply(lambda row: row.symbol.split('_')[0],
                                     axis=1)

    # Filter all the pairs to get only the ones for a given base_currency
    df = df[df['base_currency'] == context.base_currency]

    # Filter all pairs to ensure that pair existed in the current date range
    df = df[df.start_date < lookback_date]
    df = df[df.end_daily >= current_date]
    context.coins = symbols(*df.symbol)  # convert all the pairs to symbols

    return df.symbol.tolist()


# Replace all NA, NAN or infinite values with its nearest value
def fill(series):
    if isinstance(series, pd.Series):
        return series.replace([np.inf, -np.inf], np.nan).ffill().bfill()
    elif isinstance(series, np.ndarray):
        return pd.Series(series).replace(
            [np.inf, -np.inf], np.nan
        ).ffill().bfill().values
    else:
        return series

earn = {
        'fastL': [],
        'fastS': [],
        'slowL': [],
        'slowS': []
        }
if __name__ == '__main__':
    start_date = pd.to_datetime('2017-6-30', utc=True)
    end_date = pd.to_datetime('2018-6-30', utc=True)

    performance = run_algorithm(start=start_date, end=end_date,
                                capital_base=500000.0,  # amount of base_currency
                                initialize=initialize,
                                handle_data=handle_data1,
                                analyze=analyze,
                                exchange_name='bitfinex',
                                data_frequency='minute',
                                quote_currency='usd',
                                live=False,
                                live_graph=False,
                                algo_namespace='turtle')
    '''
    performance = run_algorithm(start=start_date, end=end_date,
                                capital_base=500000.0,  # amount of base_currency
                                initialize=initialize,
                                handle_data=handle_data,
                                analyze=analyze,
                                exchange_name='bitfinex',
                                data_frequency='minute',
                                quote_currency='usd',
                                live=False,
                                live_graph=False,
                                algo_namespace='turtle')
    '''
