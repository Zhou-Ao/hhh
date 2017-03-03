# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 10:55:20 2017

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
#    #Engulf
#    for bar2atr in np.arange(1.1, 1.5, 0.05):
#        for body2atr in np.arange(0.6, 0.9, 0.05):
#            print(ticker + ': Engulf1 and Engulf2')
#            print((bar2atr, body2atr))
#            chart.AddEngulf1(bar2atr, body2atr)
#            chart.AddEngulf2(bar2atr, body2atr)
    
    for shadow2bar in np.arange(0.05, 0.2, 0.05): 
        for body2atr in np.arange(0.6, 0.9, 0.04):
            print(ticker + ': Engulf')
            chart.AddEngulf(shadow2bar, body2atr)
     
#    #InsideBar
#    for bart22atr in np.arange(0.6, 0.9, 0.05):
#        print(ticker + ': InsideBar1')
#        print((bart22atr))
#        chart.AddInsideBar1(bart22atr)
#        for bart12atr in np.arange(0.6, 0.9, 0.05):
#            for bodyt12atr in np.arange(0.6, 0.9, 0.05):
#                print(ticker + ': InsideBar2')
#                print((bart22atr, bart12atr, bodyt12atr))
#                chart.AddInsideBar2(bart22atr, bart12atr, bodyt12atr)

    for body2atr_t2 in np.arange(0.4, 0.7, 0.05):
        for body2atr in np.arange(0.4, 0.7, 0.05):
            print(ticker + ': InsideBar')
            chart.AddInsideBar(body2atr_t2, body2atr)
#    
#    #Hammer
#    for bar2atr in np.arange(0.6, 0.9, 0.05):
    for body2atr in np.arange(0.05, 0.2, 0.05):
        for lowershadow2atr in np.arange(0.4, 0.8, 0.05):
            for uppershadow2atr in np.arange(0.05, 0.2, 0.05):
                    print(ticker)
                    print((0.0, body2atr, lowershadow2atr, uppershadow2atr))
                    # the first parameter of hammer4 is not used
                    chart.AddHammer4(0.0, body2atr, lowershadow2atr, uppershadow2atr)
#                    
#                    
    #CombInsideBar
    chart.AddPureInsideBar()
    for bar2atr in np.arange(0.6, 0.9, 0.05):
        print(ticker + ': InsideBarComb')
        print((bar2atr))
        chart.AddCombInsideBar(bar2atr)                

    
    # generate signal list (all the signal column names)                    
    signalList = [signal for signal in chart.chartDf.columns 
                  if ('Engulf' in signal) or ('InsideBar' in signal) or ('Hammer' in signal)]
    if 'InsideBarPure' in signalList:
        signalList.remove('InsideBarPure')
    
    #--------------------------------------------------------------------------
    # Backtest Signals
    #--------------------------------------------------------------------------
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