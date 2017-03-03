# -*- coding: utf-8 -*-
"""
Created on Wed Feb 01 09:18:37 2017

@author: strategy.intern.2
"""

import datetime
import pandas as pd
import tia.bbg.datamgr as dm
from candle.candle import CandleChart
from backtesting.backtest import CandleBacktester

# read input data
ticker = 'EURUSD BGN Curncy'
#startTime = datetime.date(2009,9,10)
#endTime = datetime.date(2017,1,31)
endDate = datetime.date.today()
startDate = endDate - datetime.timedelta(50)


# retrive data from bloomblog
mgr = dm.BbgDataManager()
curncy = mgr[ticker]

rawDf = curncy.get_historical(['PX_OPEN', 'PX_HIGH', 'PX_LOW', 'PX_LAST'], 
                              startDate.strftime('%m/%d/%Y'), endDate.strftime('%m/%d/%Y'))

# read data from excel
#rawDf = pd.read_excel('input.xlsx')

# create candlestick
chart = CandleChart(ticker, 'Day', 1, rawDf.index.tolist(), 
    rawDf.PX_OPEN.tolist(), rawDf.PX_HIGH.tolist(), rawDf.PX_LOW.tolist(), rawDf.PX_LAST.tolist())

# plot candlestick chart, maybe need couple of seconds to render
#chart.PlotChart(startTime, startTime + datetime.timedelta(20))

# calculate candle metrics
chart.CaculateBarMetrics()
chart.CaculateATR()

# Add trading signals
#chart.AddEngulf1(1.7, 0.7)
#chart.AddEngulf1(1.25, 0.7)
#chart.AddEngulf1(1.15, 0.6)

chart.AddHammer1(0.8, 0.38, 0.28, 2, 0.35)
chart.AddHammer2(0.8, 0.44, 0.55, 0.7)
chart.AddHammer3(0.8, 0.5, 0.15, 0.2, 0.7)

#chart.AddInsideBar1(0.9)
#chart.AddInsideBar2(0.8, 0.8, 0.7)

#chart.AddPureInsideBar()
#chart.AddCombInsideBar(0.6)

# create backtest engine
backtester = CandleBacktester(ticker, startDate, endDate)
holdingPeriod = 3
#backtester.Backtest(['Engulf1.0', 'Engulf1.1', 'Engulf1.2', 'Hammer1.0', 'InsideBar1.0', 'CombInsideBar1.0'], 
#                         chart.chartDf, chart.signalPara, holdingPeriod, 'Daily')
backtester.Backtest(['Hammer1.0', 'Hammer2.0', 'Hammer3.0'], 
                         chart.chartDf, chart.signalPara, holdingPeriod, 'Daily')