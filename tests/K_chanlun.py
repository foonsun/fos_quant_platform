'''
from pandas import DataFrame, Series
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import dates as mdates
from matplotlib import ticker as mticker
from matplotlib.finance import candlestick_ohlc
from matplotlib.dates import DateFormatter, WeekdayLocator, DayLocator, MONDAY,YEARLY
from matplotlib.dates import MonthLocator,MONTHLY
import datetime as dt
import pylab
'''
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import ticker as mticker
from mpl_finance import candlestick_ohlc
from matplotlib import dates as mdates
from pandas import DataFrame,Series
from matplotlib.dates import DateFormatter, WeekdayLocator, DayLocator, MinuteLocator,MONDAY,YEARLY
from matplotlib.dates import MonthLocator,MONTHLY
import matplotlib.patches as patches
import datetime as dt
import csv
import os
from matplotlib.dates import date2num
import talib as ta
import numpy as np


#C:\Users\wengyiming\Downloads\SAMPLE-binance-candle-data-push-2018-01-31\2018-01-31\BTCUSDT'

# def date_to_num(dates):
#     num_time = []
#     for date in dates:
#         print(date)
#         date_time = dt.datetime.strptime(date,'%Y/%m/%d %H:%M')
#         num_date = mdates.date2num(date)
#         num_time.append(num_date)
#     return num_time

def readstkData(filepaths, interval):
    dfs = []
    for rootpath in filepaths:
        file_list = os.listdir(rootpath)
        for file in file_list:
            if file.endswith(interval+'.csv'):
                file_path = os.path.join(rootpath, file)
                df = pd.read_csv(file_path, skiprows=1) 
                dfs.append(df)
    df = [] 
    df = pd.concat(dfs)
    df['candle_begin_time'] = pd.to_datetime(df['candle_begin_time'])
    df.sort_values('candle_begin_time', inplace=True)
    #df = df[0:2500]
    returndata = df

# Wash data
#    returndata = returndata.sort_index()
    #returndata.drop(['quote_volume','trade_num'],axis=1,inplace=True)
#    print(returndata)
#    returndata.columns = ['Open', 'High', 'Close', 'Low', 'Volume']
    returndata.columns=['Time','Open', 'High', 'Low', 'Close', 'Volume']
    returndata['Time']=date2num(returndata['Time'])
    return returndata

def drawing_candle():

    exchange = 'bitfinex'
    symbol = 'ETHUSD'
    interval = '30T'
    time_period = ['2018-01','2018-02','2018-03','2018-04','2018-05','2018-06','2018-07','2018-08','2018-09','2018-10']
    absdir = os.path.dirname(os.path.abspath(__file__))
    filepaths = []
    for period in time_period:
        daylinefilepath = os.path.join(absdir,exchange,symbol,period)
        filepaths.append(daylinefilepath)
    days = readstkData(filepaths,interval)

    # drop the date index from the dateframe & make a copy
    daysreshape = days.reset_index()
    # convert the datetime64 column in the dataframe to 'float days'
    #daysreshape['Time'] = mdates.date2num(daysreshape['Time'].astype(dt.date))
    # clean day data for candle view
    daysreshape.drop('Volume', axis=1, inplace=True)
    daysreshape = daysreshape.reindex(columns=['Time', 'Open', 'High', 'Low', 'Close'])

    #Av1 = movingaverage(daysreshape.Close.values, MA1)
    #Av2 = movingaverage(daysreshape.Close.values, MA2)
    MA2=5
    MACD_FAST = 12
    MACD_SLOW = 26
    MACD_SIGNAL = 9
    
    analysis = pd.DataFrame(index = mdates.num2date(daysreshape.Time))
    analysis['macd'], analysis['macdSignal'], analysis['macdHist'] = ta.MACD(daysreshape.Close.as_matrix(), fastperiod=MACD_FAST, slowperiod=MACD_SLOW, signalperiod=MACD_SIGNAL)
    analysis['macd_test'] = np.where((analysis.macd > analysis.macdSignal), 1, 0)
    
    SP = len(daysreshape.Time.values[MA2 - 1:])
    print(SP)
    
    # Prepare plot
    fig, (ax1, ax3) = plt.subplots(2, 1, sharex=True)
    ax1.set_yticks([])
    #size plot
    fig.set_size_inches(15,30)
    
    #fig = plt.figure(facecolor='#07000d', figsize=(14, 18))
    ax1 = fig.add_subplot(211)
    candlestick_ohlc(ax1, daysreshape.values[-SP:], width=0.0014, colorup='#ff1717', colordown='#53c156')
    ax1.grid(True, color='k',linestyle='--')
    ax1.set_xticks([])
    ax1.set_ylabel('ETH price', size=12)
    #plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='upper'))
    #ax1.tick_params(axis='x', colors='w')
    #plt.xticks(rotation=70)

    absdir = os.path.dirname(os.path.abspath(__file__))
    file_list = os.listdir(absdir)
    fenbi_files = []
    xianduan_files = []
    zhongshu_files = []
    fenbi_name = 'allfenbi.csv'
    xianduan_name = 'allxianduan.csv'
    zhongshu_name = 'allzhongshu.csv'
    for filecsv in file_list:
        if filecsv.startswith('fenbi'):
            fenbi_files.append(filecsv)
        elif filecsv.startswith('xianduan'):
            xianduan_files.append(filecsv)
        elif filecsv.startswith('zhongshu'):
            zhongshu_files.append(filecsv)
    # concat fenbi
    df = pd.read_csv(fenbi_files[0])
    df.to_csv(fenbi_name, index=False)
    for i in range(1,len(fenbi_files)):
        df = pd.read_csv(fenbi_files[i])
        df.to_csv(fenbi_name, index=False, header=False, mode='a+')
    df = pd.read_csv(fenbi_name)
    df['candle_begin_time'] = pd.to_datetime(df['candle_begin_time'])
    df.sort_values('candle_begin_time', inplace=True)
    df.to_csv(fenbi_name, index=False)
    # concat xianduan
    df = pd.read_csv(xianduan_files[0])
    df.to_csv(xianduan_name, index=False)
    for i in range(1,len(xianduan_files)):
        df = pd.read_csv(xianduan_files[i])
        df.to_csv(xianduan_name, index=False, header=False, mode='a+')
    df = pd.read_csv(xianduan_name)
    df['candle_begin_time'] = pd.to_datetime(df['candle_begin_time'])
    df.sort_values('candle_begin_time', inplace=True)
    df.to_csv(xianduan_name, index=False)
    # concat zhongshu
    df = pd.read_csv(zhongshu_files[0])
    df.to_csv(zhongshu_name, index=False)
    for i in range(1,len(zhongshu_files)):
        df = pd.read_csv(zhongshu_files[i])
        df.to_csv(zhongshu_name, index=False, header=False, mode='a+')
    df = pd.read_csv(zhongshu_name)
    df['begin_time'] = pd.to_datetime(df['begin_time'])
    df.sort_values('begin_time', inplace=True)
    df.to_csv(zhongshu_name, index=False)
    
    x_axis = []
    y_axis = []
    with open(fenbi_name, 'r') as f:
    	csv_reader = csv.reader(f)
    	for item in csv_reader:
    		if item[0] == 'candle_begin_time':
    			continue
    		x_axis.append(mdates.date2num(pd.to_datetime(item[0])))
    		y_value = item[1] if item[3]=='Y' else item[2]
    		y_axis.append(float(y_value))
    plt.plot(x_axis, y_axis)

    x2_axis = []
    y2_axis = []

    with open(xianduan_name, 'r') as f:
    	csv_reader = csv.reader(f)
    	for item in csv_reader:
    		if item[0] == 'candle_begin_time':
    			continue
    		x2_axis.append(mdates.date2num(pd.to_datetime(item[0])))
    		y_value = item[1] if item[3]=='Y' else item[2]
    		y2_axis.append(float(y_value))

    plt.plot(x2_axis, y2_axis,'--')
    
    with open(zhongshu_name, 'r') as f:
        csv_reader = csv.reader(f)
        for item in csv_reader:
            if item[0] == 'begin_time':
                continue 
            ax1.add_patch(
                    patches.Rectangle(
                        (mdates.date2num(pd.to_datetime(item[0])), float(item[3])),
                        mdates.date2num(pd.to_datetime(item[1])) - mdates.date2num(pd.to_datetime(item[0])),
                        float(item[2])-float(item[3]),
                        edgecolor='r',
                        facecolor='none'
                        )
                )
   
    # Draw MACD computed with Talib
    ax3.set_xlabel('Date', size=12)
    ax3.set_ylabel('MACD: '+ str(MACD_FAST) + ', ' + str(MACD_SLOW) + ', ' + str(MACD_SIGNAL), size=12)
    analysis.macd.plot(ax=ax3, color='b', label='Macd')
    analysis.macdSignal.plot(ax=ax3, color='g', label='Signal')
    analysis.macdHist.plot(ax=ax3, color='r', label='Hist')
    ax3.axhline(0, lw=2, color='0')
    handles, labels = ax3.get_legend_handles_labels()
    ax3.legend(handles, labels)
    #ax3.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
    plt.xticks(rotation=70)
    #plt.show()
    filename = exchange + symbol + str(time_period) + interval + '.png'
    symbolpath = os.path.join(absdir,symbol)
    if not os.path.isdir(symbolpath):
        os.mkdir(symbolpath)
    filepath = os.path.join(absdir,symbol,filename)
    fig.savefig(filepath)

drawing_candle()
