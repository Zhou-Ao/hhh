# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 11:12:03 2017

@author: strategy.intern.2
"""

import sys
# include the project path in the python path
projectPath = 'U:/Python Project/MagicCandle/' #need to change dir
sys.path.append(projectPath)

import datetime
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
startDate = endDate - datetime.timedelta(300)
# regular expression
pattern = CandleSignal.GetFloatPattern()
# ticker
tickerList = CandleUtility.GetTickerList()
              

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
                                  startDate.strftime('%m/%d/%Y'), endDate.strftime('%m/%d/%Y'),
                                    period = 'WEEKLY')
    
    
    # create candlestick
    chartDict[ticker] = CandleChart(tickerList, 'Week', 1, rawDf.index.tolist(), 
        rawDf.PX_OPEN.tolist(), rawDf.PX_HIGH.tolist(), rawDf.PX_LOW.tolist(), rawDf.PX_LAST.tolist())
        
    # calculate candle metrics
    chartDict[ticker].CaculateBarMetrics()
    chartDict[ticker].CaculateATR()
    
    print('Adding Signals: ' + ticker)
    # Add signals
    chartDict[ticker].AddHammer(0.7, 0.38, 0.28, 2, 0.35, 0.44, 0.55, 0.7, 0.5, 0.15, 0.2, 0.7)
    chartDict[ticker].AddEngulf(0.1, 0.8)
    chartDict[ticker].AddInsideBar(0.7, 0.7)
    
    chartDict[ticker].chartDf.rename(columns={
                                            'InsideBar0.0' : 'InsideBar',
                                            'Hammer0.0' : 'Hammer',
                                            'Engulf0.0' : 'Engulf'}, inplace=True)

    
#------------------------------------------------------------------------------
# Export Final Result
#------------------------------------------------------------------------------
#finalDate = endDate
final_df = pd.DataFrame()

# loop from 20 days before endDate (ususally set to today) to most recent date
for ticker in tickerList:
    for date in chartDict[ticker].chartDf.index[-20:]:
        for signal in ['Engulf', 'InsideBar', 'Hammer', 'InsideComb']:
            final_df = pd.concat([final_df, CandleSignal.CreateSimpleSummaryDf(signal, ticker, chartDict[ticker], date)], axis = 0)
            
final_df = final_df.sort_index(ascending = False)

if len(final_df) > 0:
    CandleSignal.AddDateColumn(final_df, 'Weekly')
    final_df.to_csv('.\Signals\SimpleWeeklySignal' + datetime.date.today().strftime('%Y%m%d') + '.csv')