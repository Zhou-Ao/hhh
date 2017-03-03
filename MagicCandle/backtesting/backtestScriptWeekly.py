# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 10:32:12 2017

@author: strategy.intern.2
"""

import datetime
import pandas as pd
import numpy as np
import tia.bbg.datamgr as dm
from candle.candle import CandleChart
from utility.utility import CandleUtility
from backtesting.backtest import CandleBacktester

#------------------------------------------------------------------------------
# Initailize Settings
#------------------------------------------------------------------------------
# read input data
tickerList = CandleUtility.GetTickerList()

# backtest start date and end date              
#startTime = datetime.date(2009,9,10)
#endTime = datetime.date(2017,1,31)
#endTime = datetime.date.today()
endDate = datetime.date(2017,2,6)
startDate = datetime.date(2009,1,1)

# create bloomberg engine
mgr = dm.BbgDataManager()

# initialize backtest result data frame
result_df = pd.DataFrame(columns = ['Curncy', 'Signal', 'Parameters', 'Frequency', 'HoldingPeriod', 'Period', 
                                        'TotalHits', 'TotalWins', 'HitRate', 'CumReturn',
                                        'MaxReturn', 'AveDrawdown', 'MaxDrawdown'])
for ticker in tickerList:
    # loop curncy
    curncy = mgr[ticker]
    # get blp data
    rawDf = curncy.get_historical(['PX_OPEN', 'PX_HIGH', 'PX_LOW', 'PX_LAST'], 
                              startDate.strftime('%m/%d/%Y'), endDate.strftime('%m/%d/%Y'),
                                period='WEEKLY')
    
    chart = CandleChart(ticker, 'Week', 1, rawDf.index.tolist(), 
        rawDf.PX_OPEN.tolist(), rawDf.PX_HIGH.tolist(), rawDf.PX_LOW.tolist(), rawDf.PX_LAST.tolist())
    
    # calculate candle metrics
    chart.CaculateBarMetrics()
    chart.CaculateATR()
    
    
    #--------------------------------------------------------------------------
    # Add Trading Signals
    #--------------------------------------------------------------------------
    print('Adding signals: ' + ticker)
    chart.AddHammer(0.7, 0.38, 0.28, 2, 0.35, 0.44, 0.55, 0.7, 0.5, 0.15, 0.2, 0.7)
    chart.AddEngulf(0.1, 0.8)
    chart.AddInsideBar(0.6, 0.6)
    chart.AddInsideBar(0.5, 0.5)
    chart.AddInsideBar(0.4, 0.4)

    
    # generate signal list (all the signal column names)                    
    signalList = [signal for signal in chart.chartDf.columns 
                  if ('Engulf' in signal) or ('InsideBar' in signal) or ('Hammer' in signal)]
    if 'InsideBarPure' in signalList:
        signalList.remove('InsideBarPure')
    
    #--------------------------------------------------------------------------
    # Backtest Signals
    #--------------------------------------------------------------------------
    print('Backtesting signals: ' + ticker)
    # create backtest  
    backtester0 = CandleBacktester(ticker, startDate, endDate, 'Weekly')
    backtester1 = CandleBacktester(ticker, startDate, datetime.date(2012, 1,1), 'Weekly')
    backtester2 = CandleBacktester(ticker, datetime.date(2012, 1, 1), datetime.date(2015, 1,1), 'Weekly')
    backtester3 = CandleBacktester(ticker, datetime.date(2015, 1, 1), endDate, 'Weekly')

    # backtest for different holding period
    for holdingPeriod in [3, 5]:
        result_temp = backtester0.Backtest(signalList, chart.chartDf, chart.signalPara, holdingPeriod)
        result_df = result_df.append(result_temp, ignore_index=True)
        
        result_temp = backtester1.Backtest(signalList, chart.chartDf, chart.signalPara, holdingPeriod)
        result_df = result_df.append(result_temp, ignore_index=True)
        
        result_temp = backtester2.Backtest(signalList, chart.chartDf, chart.signalPara, holdingPeriod)
        result_df = result_df.append(result_temp, ignore_index=True)
        
        result_temp = backtester3.Backtest(signalList, chart.chartDf, chart.signalPara, holdingPeriod)
        result_df = result_df.append(result_temp, ignore_index=True)
        
#------------------------------------------------------------------------------
# Save Backtest Result
#------------------------------------------------------------------------------        
store = pd.HDFStore('WeeklyBacktest' + datetime.date.today().strftime('%Y%m%d') + '.h5')
store['weekly'] = result_df
store.close()