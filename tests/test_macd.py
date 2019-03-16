# Run Command
# catalyst run --start 2017-1-1 --end 2017-11-1 -o talib_simple.pickle \
#   -f talib_simple.py -x poloniex
#
# Description
# Simple TALib Example showing how to use various indicators
# in you strategy. Based loosly on
# https://github.com/mellertson/talib-macd-example/blob/master/talib-macd-matplotlib-example.py

import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import talib as ta
from logbook import Logger
from matplotlib.dates import date2num
from mpl_finance import candlestick_ohlc

from catalyst import run_algorithm
from catalyst.api import (
    order,
    order_target_percent,
    symbol,
)
from catalyst.exchange.utils.stats_utils import get_pretty_stats

algo_namespace = 'talib_sample'
log = Logger(algo_namespace)


def initialize(context):
    log.info('Starting TALib macd')

    context.ASSET_NAME = 'BTC_USD'
    context.asset = symbol(context.ASSET_NAME)

    context.ORDER_SIZE = 10
    context.SLIPPAGE_ALLOWED = 0.05

    context.errors = []

    # Bars to look at per iteration should be bigger than SMA_SLOW
    context.BARS = 365
    context.COUNT = 0
    
    context.macds = pd.Series()
    context.macdSignals = pd.Series()
    context.macdHists = pd.Series()

    # Technical Analysis Settings
    context.MACD_FAST = 12
    context.MACD_SLOW = 26
    context.MACD_SIGNAL = 9
 
    # 买卖点
    context.BTC_BUY_TIME = [pd.Timestamp('2018-03-01 23:59:00',tz='UTC'), pd.Timestamp('2018-04-01 23:59:00',tz='UTC'), pd.Timestamp('2018-05-01 23:59:00',tz='UTC'), pd.Timestamp('2018-06-01 23:59:00',tz='UTC')]
    context.BTC_SELL_TIME = [pd.Timestamp('2018-07-01 23:59:00',tz='UTC'), pd.Timestamp('2018-08-01 23:59:00',tz='UTC'), pd.Timestamp('2018-09-01 23:59:00',tz='UTC'),pd.Timestamp('2018-10-01 23:59:00',tz='UTC')]

def _handle_data(context, data):
    # Get price, open, high, low, close
    prices = data.history(
        context.asset,
        bar_count=context.BARS,
        fields=['price', 'open', 'high', 'low', 'close'],
        frequency='1d')

    # Create a analysis data frame
    analysis = pd.DataFrame(index=prices.index)

    # MACD, MACD Signal, MACD Histogram
    analysis['macd'], analysis['macdSignal'], analysis['macdHist'] = ta.MACD(
        prices.close.as_matrix(), fastperiod=context.MACD_FAST,
        slowperiod=context.MACD_SLOW, signalperiod=context.MACD_SIGNAL)

    # MACD over Signal Crossover
    analysis['macd_test'] = np.where((analysis.macd > analysis.macdSignal), 1,
                                     0)
    # Save the prices and analysis to send to analyze
    context.prices = prices
    context.analysis = analysis
    context.price = data.current(context.asset, 'price')
    context.date = data.current_dt
    makeOrders(context, analysis)

    # Log the values of this bar
    logAnalysis(analysis)


def handle_data(context, data):
    log.info('handling bar {}'.format(data.current_dt))
    try:
        _handle_data(context, data)
    except Exception as e:
        log.warn('aborting the bar on error {}'.format(e))
        context.errors.append(e)

    log.info('completed bar {}, total execution errors {}'.format(
        data.current_dt,
        len(context.errors)
    ))

    if len(context.errors) > 0:
        log.info('the errors:\n{}'.format(context.errors))


def analyze(context, perf):
    chart(context, context.prices, context.analysis, perf)
    pass


def makeOrders(context, analysis):
    if context.asset in context.portfolio.positions:

        # Current position
        position = context.portfolio.positions[context.asset]

        if (position == 0):
            log.info('Position Zero')
            return

        # Cost Basis
        cost_basis = position.cost_basis

        log.info(
            'Holdings: {amount} @ {cost_basis}'.format(
                amount=position.amount,
                cost_basis=cost_basis
            )
        )

        # Sell when holding and got sell singnal
        if isSell(context, analysis):
            profit = (context.price * position.amount) - (
                cost_basis * position.amount)
            order_target_percent(
                asset=context.asset,
                target=0,
                limit_price=context.price * (1 - context.SLIPPAGE_ALLOWED),
            )
            log.info(
                'Sold {amount} @ {price} Profit: {profit}'.format(
                    amount=position.amount,
                    price=context.price,
                    profit=profit
                )
            )
        else:
            log.info('no buy or sell opportunity found')
    else:
        # Buy when not holding and got buy signal
        if isBuy(context, analysis):
            order(
                asset=context.asset,
                amount=context.ORDER_SIZE,
                limit_price=context.price * (1 + context.SLIPPAGE_ALLOWED)
            )
            log.info(
                'Bought {amount} @ {price}'.format(
                    amount=context.ORDER_SIZE,
                    price=context.price
                )
            )


def isBuy(context, analysis):
    # Bullish SMA Crossover
    # Bullish MACD
    # if (getLast(analysis, 'macd_test') == 1):
    #   return True
    if context.date in context.BTC_BUY_TIME:
        return True
    # # Bullish Stochastics
    # if(getLast(analysis, 'stoch_over_sold') == 1):
    #     return True

    # # Bullish RSI
    # if(getLast(analysis, 'rsi_over_sold') == 1):
    #     return True

    return False


def isSell(context, analysis):
    # Bearish SMA Crossover
    # if (getLast(analysis, 'macd_test') == 0):
    #   return True
    if context.date in context.BTC_SELL_TIME:
        return True
    # # Bearish Stochastics
    # if(getLast(analysis, 'stoch_over_bought') == 0):
    #     return True

    # # Bearish RSI
    # if(getLast(analysis, 'rsi_over_bought') == 0):
    #     return True

    return False


def chart(context, prices, analysis, perf):
    fig = plt.figure()
    ax1 = fig.add_subplot(411)
    perf.portfolio_value.plot(ax=ax1)
    ax1.set_ylabel('portfolio value')
    
    ax2 = fig.add_subplot(412,sharex=ax1)
    perf.sharpe.plot()
    ax2.set_ylabel('sharpe')
    
    ax3 = fig.add_subplot(413,sharex=ax1)
    perf.benchmark_period_return.plot()
    ax3.set_ylabel('benchmark period return')
    
    ax4 = fig.add_subplot(414,sharex=ax1)
    perf.pnl.plot()
    ax4.set_ylabel('pnl')

    plt.show()


def logAnalysis(analysis):
    # Log only the last value in the array
    ''' 
    log.info('- macd:           {:.2f}'.format(getLast(analysis, 'macd')))
    log.info(
        '- macdSignal:     {:.2f}'.format(getLast(analysis, 'macdSignal')))
    log.info('- macdHist:       {:.2f}'.format(getLast(analysis, 'macdHist')))
    log.info('- macd_test:      {}'.format(getLast(analysis, 'macd_test')))
    '''
def getLast(arr, name):
    return arr[name][arr[name].index[-1]]


if __name__ == '__main__':
    run_algorithm(
        capital_base=10000,
        data_frequency='daily',
        initialize=initialize,
        handle_data=handle_data,
        analyze=analyze,
        exchange_name='bitfinex',
        quote_currency='usd',
        start=pd.to_datetime('2018-6-1', utc=True),
        end=pd.to_datetime('2018-8-31', utc=True),
    )