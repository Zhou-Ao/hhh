# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 10:02:37 2017

@author: strategy.intern.2
"""
import datetime
import re
import pandas as pd
import numpy as np

import tia.bbg.datamgr as dm
from candle.candle import CandleChart
from utility.utility import CandleUtility
from candlesignal import CandleSignal

#------------------------------------------------------------------------------
# Initailize Settings
#------------------------------------------------------------------------------
# date
endDate = datetime.date.today() - datetime.timedelta(1)
startDate = endDate - datetime.timedelta(30)
# regular expression
pattern = CandleSignal.GetFloatPattern()
# ticker
tickerList = CandleUtility.GetTickerList()
              
#------------------------------------------------------------------------------
# Load Signal Parameters
#------------------------------------------------------------------------------
#store = pd.HDFStore('signal.h5')
store = pd.HDFStore('DailySignal20170224.h5') # modify the store file name accordingly
signal_df = store['signal']
store.close()

signal_df['Parameters'] = signal_df['Parameters'].apply(lambda x: tuple(re.findall(pattern, x)))

#------------------------------------------------------------------------------
# Add Signals
#------------------------------------------------------------------------------
# create bloomblog data engine
mgr = dm.BbgDataManager()

chartDict = {}

for ticker in tickerList:
    print('Processing: ' + ticker)
    # retrive data from bloomblog
    curncy = mgr[ticker]
    
    rawDf = curncy.get_historical(['PX_OPEN', 'PX_HIGH', 'PX_LOW', 'PX_LAST'], 
                                  startDate.strftime('%m/%d/%Y'), endDate.strftime('%m/%d/%Y'))
    
    
    # create candlestick
    chartDict[ticker] = CandleChart(tickerList, 'Day', 1, rawDf.index.tolist(), 
        rawDf.PX_OPEN.tolist(), rawDf.PX_HIGH.tolist(), rawDf.PX_LOW.tolist(), rawDf.PX_LAST.tolist())
        
    # calculate candle metrics
    chartDict[ticker].CaculateBarMetrics()
    chartDict[ticker].CaculateATR()
    
    print('Adding Signals: ' + ticker)
    # Add signals
    CandleSignal.AddSignals(ticker, chartDict[ticker], signal_df)
    
#------------------------------------------------------------------------------
# Aggregate Settings
#------------------------------------------------------------------------------            
# for example, aggregate Engulf0, Engulf1 and Engulf2 to Engulf
for ticker in tickerList:
    CandleSignal.AggregateSignals(ticker, chartDict[ticker], signal_df)
    
#------------------------------------------------------------------------------
# Export Final Result
#------------------------------------------------------------------------------
#finalDate = endDate
final_df = pd.DataFrame()

# loop from 20 days before endDate (ususally set to today) to most recent date
for ticker in tickerList:
    for date in chartDict[ticker].chartDf.index[-20:]:
        for signal in ['Engulf', 'InsideBar', 'Hammer', 'InsideComb']:
            final_df = pd.concat([final_df, CandleSignal.CreateSummaryDf(signal, ticker, chartDict[ticker], date)], axis = 0)
            
final_df = final_df.sort_index(ascending = False)

if len(final_df) > 0:
    CandleSignal.AddDateColumn(final_df, 'Daily')
    final_df.to_csv('./Signals/DailySignal' + datetime.date.today().strftime('%Y%m%d') + '.csv')

