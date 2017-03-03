# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 16:17:17 2017

@author: strategy.intern.2
"""

import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import date2num
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
from matplotlib.finance import candlestick_ohlc
from shape import CandleShape

class CandleChart:
    '''
    Class of Candle Chart
    '''
    
    def __init__(self, ticker, period, size, datetimeList, openPriceList, 
                highPriceList, lowPriceList, closePriceList, 
                preClosePriceList = None):
        # chart particulars
        self.ticker = ticker
        self.period = self._validateBarPeriod(period)
        self.size = size
        
        # sort list, time ascending        
        if datetimeList[0] > datetimeList[-1]:
            datetimeList.reverse()
            openPriceList.reverse()
            highPriceList.reverse()
            lowPriceList.reverse()
            closePriceList.reverse()
            if preClosePriceList is not None:
                preClosePriceList.reverse()
        
        # initialize signal dataframe
        self.signalDf = pd.DataFrame(index = datetimeList)
        self.signalNum = {'Engulf' : 
                            {
                             0 : 0,
                             1 : 0,
                             2 : 0},
                        'Hammer' : 
                            {
                             0 : 0,
                             1 : 0,
                             2 : 0,
                             3 : 0,
                             4 : 0},
                        'InsideBar' : 
                            {
                             0 : 0,
                             1 : 0,
                             2 : 0},
                        'InsideBarComb' :
                            {0 : 0}
                        }
                             
        self.signalPara = {}

        
        # validate list size and generate dataframe
        if preClosePriceList is None:
            if(len(datetimeList) == len(openPriceList) == len(highPriceList)
                == len(lowPriceList) == len(closePriceList)):        
                self.chartDf = pd.DataFrame({
                        'Open'     : openPriceList,
                        'High'     : highPriceList,
                        'Low'      : lowPriceList,
                        'Close'    : closePriceList,
                        'PreClose' : [np.nan] + closePriceList[:-1]
                        },
                        index = datetimeList, 
                        columns = ['Open', 'High', 'Low', 'Close', 'PreClose'])
                
                self.chartDf = self.chartDf.sort_index()
            else:
                raise Exception('CandleChart: Unmatched list size!')
        else:
            if(len(datetimeList) == len(openPriceList) 
                == len(highPriceList)
                == len(lowPriceList) 
                == len(closePriceList) 
                == len(preClosePriceList)):        
                self.chartDf = pd.DataFrame({
                        'Open'     : openPriceList,
                        'High'     : highPriceList,
                        'Low'      : lowPriceList,
                        'Close'    : closePriceList,
                        'PreClose' : preClosePriceList
                        },
                        index = datetimeList, 
                        columns = ['Open', 'High', 'Low', 'Close', 'PreClose'])
                
                self.chartDf = self.chartDf.sort_index()
            else:
                raise Exception('CandleChart: Unmatched list size!')
            
    def CaculateBarMetrics(self):
        self.chartDf = self.chartDf.sort_index()
        
        # body = abs(close - open)
        self.chartDf['Body'] = np.abs(self.chartDf.Close - self.chartDf.Open)
        # upper shadow = high - max(open, close)
        self.chartDf['UpperShadow'] = self.chartDf.apply(lambda row:
            row.High - np.max([row.Open, row.Close]), axis = 1)
        # lower shadow = min(open, close) - low
        self.chartDf['LowerShadow'] = self.chartDf.apply(lambda row:
            np.min([row.Open, row.Close]) - row.Low, axis = 1)
        # bar = high - low
        self.chartDf['Bar'] = self.chartDf.High - self.chartDf.Low
        
        # ratios
        self.chartDf['UpperShadowToBody'] \
            = self.chartDf.UpperShadow / np.abs(self.chartDf.Body)
        self.chartDf['LowerShadowToBody'] \
            = self.chartDf.LowerShadow / np.abs(self.chartDf.Body)
        self.chartDf['UpperShadowToBar'] \
            = self.chartDf.UpperShadow / self.chartDf.Bar
        self.chartDf['LowerShadowToBar'] \
            = self.chartDf.LowerShadow / self.chartDf.Bar
        self.chartDf['UpperShadowToLowerShadow'] \
            = self.chartDf.UpperShadow / self.chartDf.LowerShadow
        self.chartDf['LowerShadowToUpperShadow'] \
            = self.chartDf.LowerShadow / self.chartDf.UpperShadow
    
    def CaculateATR(self, window = 5, method = 'arithmetic'):
        self.chartDf = self.chartDf.sort_index()
        
        # TR and ATR
        self.chartDf['TR'] = self.chartDf.apply(lambda row:
            np.max([row.High, row.PreClose]) - np.min([row.Low, row.PreClose]),
                  axis = 1)
        if method == 'arithmetic':
            self.chartDf['ATR'] \
                = self.chartDf.TR.rolling(window = window).mean()            
        elif method == 'exponential':
            self.chartDf['eATR'] \
                = self.chartDf.TR.ewm(window = window).mean()
        else:
            raise Exception('CandleChart: Unknown method! Only support arithmetic/exponential!')
            
        self.chartDf['BarToATR'] = np.abs(self.chartDf.Bar) / self.chartDf.ATR
        self.chartDf['BodyToATR'] = self.chartDf.Body / self.chartDf.ATR
        
        self.chartDf['UpperShadowToATR'] = self.chartDf.UpperShadow / self.chartDf.ATR
        self.chartDf['LowerShadowToATR'] = self.chartDf.LowerShadow / self.chartDf.ATR
                    
    def PlotChart(self, startTime, endTime):
        self.chartDf = self.chartDf.sort_index()
        plot_df = self.chartDf.loc[startTime:endTime]

        fig = plt.figure()
        ax = plt.subplot2grid((1,1), (0,0))
        
        candlestick_ohlc(ax, zip(map(date2num, plot_df.index), plot_df.Open.tolist(),
            plot_df.High.tolist(), plot_df.Low.tolist(), plot_df.Close.tolist()))
        
        for label in ax.xaxis.get_ticklabels():
            label.set_rotation(45)

        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.xaxis.set_major_locator(mticker.MaxNLocator(10))
        ax.grid(True)
        
        plt.xlabel('Date')
        plt.ylabel(self.ticker)
        plt.title(self.ticker + ' ' + str(self.size) + ' ' + self.period + ' Bar')
        plt.legend()
        plt.subplots_adjust(left=0.09, bottom=0.20, right=0.94, top=0.90, wspace=0.2, hspace=0)
        plt.show()
        
    def PlotSignal(self, signalList, T):
        # check signal column in signalDf
        if not (set(signalList).issubset(self.chartDf.columns)):
            raise Exception('CandleChart: Invalid signal list!')
            
        for signal in signalList:
            signal_df = self.chartDf[self.chartDf[signal] != 0]
            for date in signal_df.index:
                self.PlotChart(date - datetime.timedelta(T), date + datetime.timedelta(T))
                
                
    def AddEngulf(self, shadow2bar, body2atr):
        '''
        Add trading signal Engulf
        '''
        self.chartDf = self.chartDf.sort_index()
        
        num = self.signalNum['Engulf'][0]
        self.signalPara['Engulf0.' + str(num)] = (shadow2bar, body2atr)
        
        self.signalDf['Engulf0.' + str(num) +'Long'] = CandleShape.EngulfLong(self.chartDf, shadow2bar, body2atr)
        self.signalDf['Engulf0.' + str(num) +'Short'] = CandleShape.EngulfShort(self.chartDf, shadow2bar, body2atr)
        
        self.chartDf['Engulf0.' + str(num)] = np.zeros([])
        self.chartDf['Engulf0.' + str(num)][self.signalDf['Engulf0.' + str(num) +'Long'] == True] = 1
        self.chartDf['Engulf0.' + str(num)][self.signalDf['Engulf0.' + str(num) +'Short'] == True] = -1
        
        self.signalNum['Engulf'][0] += 1
        
    def AddEngulf1(self, bar2atr, body2atr):
        '''
        Add trading signal Engulf1
        '''
        self.chartDf = self.chartDf.sort_index()
        
        num = self.signalNum['Engulf'][1]
        self.signalPara['Engulf1.' + str(num)] = (bar2atr, body2atr)
        
        self.signalDf['Engulf1.' + str(num) +'Long'] = CandleShape.Engulf1Long(self.chartDf, bar2atr, body2atr)
        self.signalDf['Engulf1.' + str(num) +'Short'] = CandleShape.Engulf1Short(self.chartDf, bar2atr, body2atr)
        
        self.chartDf['Engulf1.' + str(num)] = np.zeros([])
        self.chartDf['Engulf1.' + str(num)][self.signalDf['Engulf1.' + str(num) +'Long'] == True] = 1
        self.chartDf['Engulf1.' + str(num)][self.signalDf['Engulf1.' + str(num) +'Short'] == True] = -1
        
        self.signalNum['Engulf'][1] += 1

    def AddEngulf2(self, bar2atr, body2atr):
        '''
        Add trading signal Engulf2
        '''
        self.chartDf = self.chartDf.sort_index()
        
        num = self.signalNum['Engulf'][2]
        self.signalPara['Engulf2.' + str(num)] = (bar2atr, body2atr)
        
        self.signalDf['Engulf2.' + str(num) +'Long'] = CandleShape.Engulf2Long(self.chartDf, bar2atr, body2atr)
        self.signalDf['Engulf2.' + str(num) +'Short'] = CandleShape.Engulf2Short(self.chartDf, bar2atr, body2atr)
        
        self.chartDf['Engulf2.' + str(num)] = np.zeros([])
        self.chartDf['Engulf2.' + str(num)][self.signalDf['Engulf2.' + str(num) +'Long'] == True] = 1
        self.chartDf['Engulf2.' + str(num)][self.signalDf['Engulf2.' + str(num) +'Short'] == True] = -1
                     
        self.signalNum['Engulf'][2] += 1

    def AddHammer(self, bar2atr, body2atr, lowershadow2atr_1, lowershadow2uppershadow, 
                    uppdershadow2body, uppershadow2lowershadow_2, lowershadow2bar_2,
                    lowershadowplusbody2atr, lowershadow2atr_3, uppershadow2bar, uppershadow2lowershadow_3, lowershadow2bar_3):
        '''
        Add trading signal Hammer
        '''
        self.chartDf = self.chartDf.sort_index()
        
        num = self.signalNum['Hammer'][0]
        self.signalPara['Hammer0.' + str(num)] = (bar2atr, body2atr, lowershadow2atr_1, lowershadow2uppershadow, 
                    uppdershadow2body, uppershadow2lowershadow_2, lowershadow2bar_2,
                    lowershadowplusbody2atr, lowershadow2atr_3, uppershadow2bar, uppershadow2lowershadow_3, lowershadow2bar_3)

        self.signalDf['Hammer0.' + str(num) +'Long'] = CandleShape.HammerLong(self.chartDf, 
                      bar2atr, body2atr, lowershadow2atr_1, lowershadow2uppershadow, 
                    uppdershadow2body, uppershadow2lowershadow_2, lowershadow2bar_2,
                    lowershadowplusbody2atr, lowershadow2atr_3, uppershadow2bar, uppershadow2lowershadow_3, lowershadow2bar_3)
        self.signalDf['Hammer0.' + str(num) +'Short'] = CandleShape.HammerShort(self.chartDf, 
                      bar2atr, body2atr, lowershadow2atr_1, lowershadow2uppershadow, 
                    uppdershadow2body, uppershadow2lowershadow_2, lowershadow2bar_2,
                    lowershadowplusbody2atr, lowershadow2atr_3, uppershadow2bar, uppershadow2lowershadow_3, lowershadow2bar_3)
        
        self.chartDf['Hammer0.' + str(num)] = np.zeros([])
        self.chartDf['Hammer0.' + str(num)][self.signalDf['Hammer0.' + str(num) +'Long'] == True] = 1
        self.chartDf['Hammer0.' + str(num)][self.signalDf['Hammer0.' + str(num) +'Short'] == True] = -1
        
        self.signalNum['Hammer'][1] += 1

    def AddHammer1(self, bar2atr, body2atr, shadow2atr, shadow2shadow, shadow2body):
        '''
        Add trading signal Hammer1
        '''
        self.chartDf = self.chartDf.sort_index()
        
        num = self.signalNum['Hammer'][1]
        self.signalPara['Hammer1.' + str(num)] = (bar2atr, body2atr, shadow2atr, shadow2shadow, shadow2body)

        self.signalDf['Hammer1.' + str(num) +'Long'] = CandleShape.Hammer1Long(self.chartDf, 
                      bar2atr, body2atr, shadow2atr, shadow2shadow, shadow2body)
        self.signalDf['Hammer1.' + str(num) +'Short'] = CandleShape.Hammer1Short(self.chartDf, 
                      bar2atr, body2atr, shadow2atr, shadow2shadow, shadow2body)
        
        self.chartDf['Hammer1.' + str(num)] = np.zeros([])
        self.chartDf['Hammer1.' + str(num)][self.signalDf['Hammer1.' + str(num) +'Long'] == True] = 1
        self.chartDf['Hammer1.' + str(num)][self.signalDf['Hammer1.' + str(num) +'Short'] == True] = -1
        
        self.signalNum['Hammer'][1] += 1

    def AddHammer2(self, bar2atr, shadow2shadow, shadow2bar, shadowplusbody2atr):
        '''
        Add trading signal Hammer2
        '''
        self.chartDf = self.chartDf.sort_index()
        
        num = self.signalNum['Hammer'][2]
        self.signalPara['Hammer2.' + str(num)] = (bar2atr, shadow2shadow, shadow2bar, shadowplusbody2atr)
        
        self.signalDf['Hammer2.' + str(num) +'Long'] = CandleShape.Hammer2Long(self.chartDf, 
                      bar2atr, shadow2shadow, shadow2bar, shadowplusbody2atr)
        self.signalDf['Hammer2.' + str(num) +'Short'] = CandleShape.Hammer2Short(self.chartDf, 
                      bar2atr, shadow2shadow, shadow2bar, shadowplusbody2atr)
        
        self.chartDf['Hammer2.' + str(num)] = np.zeros([])
        self.chartDf['Hammer2.' + str(num)][self.signalDf['Hammer2.' + str(num) +'Long'] == True] = 1
        self.chartDf['Hammer2.' + str(num)][self.signalDf['Hammer2.' + str(num) +'Short'] == True] = -1
        
        self.signalNum['Hammer'][2] += 1

    def AddHammer3(self, bar2atr, shadow2atr_1, shadow2bar_2, shadow2shadow, shadow2bar):
        '''
        Add trading signal Hammer3
        '''
        self.chartDf = self.chartDf.sort_index()
        
        num = self.signalNum['Hammer'][3]
        self.signalPara['Hammer3.' + str(num)] = (bar2atr, shadow2atr_1, shadow2bar_2, shadow2shadow, shadow2bar)

        self.signalDf['Hammer3.' + str(num) +'Long'] = CandleShape.Hammer3Long(self.chartDf, 
                      bar2atr, shadow2atr_1, shadow2bar_2, shadow2shadow, shadow2bar)
        self.signalDf['Hammer3.' + str(num) +'Short'] = CandleShape.Hammer3Short(self.chartDf, 
                      bar2atr, shadow2atr_1, shadow2bar_2, shadow2shadow, shadow2bar)
        
        self.chartDf['Hammer3.' + str(num)] = np.zeros([])
        self.chartDf['Hammer3.' + str(num)][self.signalDf['Hammer3.' + str(num) +'Long'] == True] = 1
        self.chartDf['Hammer3.' + str(num)][self.signalDf['Hammer3.' + str(num) +'Short'] == True] = -1
        
        self.signalNum['Hammer'][3] += 1

    def AddHammer4(self, bar2atr, body2atr, lowershadow2atr, uppershadow2atr):
        '''
        Add trading signal Hammer4
        '''
        self.chartDf = self.chartDf.sort_index()
        
        num = self.signalNum['Hammer'][4]
        self.signalPara['Hammer4.' + str(num)] = (bar2atr, body2atr, lowershadow2atr, uppershadow2atr)

        self.signalDf['Hammer4.' + str(num) +'Long'] = CandleShape.Hammer4Long(self.chartDf, 
                      bar2atr, body2atr, lowershadow2atr, uppershadow2atr)
        self.signalDf['Hammer4.' + str(num) +'Short'] = CandleShape.Hammer4Short(self.chartDf, 
                      bar2atr, body2atr, lowershadow2atr, uppershadow2atr)
        
        self.chartDf['Hammer4.' + str(num)] = np.zeros([])
        self.chartDf['Hammer4.' + str(num)][self.signalDf['Hammer4.' + str(num) +'Long'] == True] = 1
        self.chartDf['Hammer4.' + str(num)][self.signalDf['Hammer4.' + str(num) +'Short'] == True] = -1
        
        self.signalNum['Hammer'][4] += 1

#    def AddInsideBar(self, body2atr_t2, body2atr):
#        '''
#        Add trading singal InsideBar
#        '''
#        self.chartDf = self.chartDf.sort_index()
#        
#        num = self.signalNum['InsideBar'][0]
#        self.signalPara['InsideBar0.' + str(num)] = (body2atr_t2, body2atr)    
#
#        self.signalDf['InsideBar0.' + str(num) +'Long'] = CandleShape.InsideBarLong(self.chartDf, 
#                      body2atr_t2, body2atr)
#        self.signalDf['InsideBar0.' + str(num) +'Short'] = CandleShape.InsideBarShort(self.chartDf, 
#                      body2atr_t2, body2atr)
#        
#        self.chartDf['InsideBar0.' + str(num)] = np.zeros([])
#        self.chartDf['InsideBar0.' + str(num)][self.signalDf['InsideBar0.' + str(num) +'Long'] == True] = 1
#        self.chartDf['InsideBar0.' + str(num)][self.signalDf['InsideBar0.' + str(num) +'Short'] == True] = -1
#        
#        self.signalNum['InsideBar'][0] += 1            

    def AddInsideBar(self, bar2atr_t2, bar2atr):
        '''
        Add trading singal InsideBar
        '''
        self.chartDf = self.chartDf.sort_index()
        
        num = self.signalNum['InsideBar'][0]
        self.signalPara['InsideBar0.' + str(num)] = (bar2atr_t2, bar2atr)    

        self.signalDf['InsideBar0.' + str(num) +'Long'] = CandleShape.InsideBarLong(self.chartDf, 
                      bar2atr_t2, bar2atr)
        self.signalDf['InsideBar0.' + str(num) +'Short'] = CandleShape.InsideBarShort(self.chartDf, 
                      bar2atr_t2, bar2atr)
        
        self.chartDf['InsideBar0.' + str(num)] = np.zeros([])
        self.chartDf['InsideBar0.' + str(num)][self.signalDf['InsideBar0.' + str(num) +'Long'] == True] = 1
        self.chartDf['InsideBar0.' + str(num)][self.signalDf['InsideBar0.' + str(num) +'Short'] == True] = -1
        
        self.signalNum['InsideBar'][0] += 1            

    def AddInsideBar1(self, bart22atr):
        '''
        Add trading singal InsideBar1
        '''
        self.chartDf = self.chartDf.sort_index()
        
        num = self.signalNum['InsideBar'][1]
        self.signalPara['InsideBar1.' + str(num)] = (bart22atr)    

        self.signalDf['InsideBar1.' + str(num) +'Long'] = CandleShape.InsideBar1Long(self.chartDf, 
                      bart22atr)
        self.signalDf['InsideBar1.' + str(num) +'Short'] = CandleShape.InsideBar1Short(self.chartDf, 
                      bart22atr)
        
        self.chartDf['InsideBar1.' + str(num)] = np.zeros([])
        self.chartDf['InsideBar1.' + str(num)][self.signalDf['InsideBar1.' + str(num) +'Long'] == True] = 1
        self.chartDf['InsideBar1.' + str(num)][self.signalDf['InsideBar1.' + str(num) +'Short'] == True] = -1
        
        self.signalNum['InsideBar'][1] += 1            

    def AddInsideBar2(self, bart22atr, bart12atr, bodyt12atr):
        '''
        Add trading singal InsideBar2
        '''
        self.chartDf = self.chartDf.sort_index()
        
        num = self.signalNum['InsideBar'][2]
        self.signalPara['InsideBar2.' + str(num)] = (bart22atr, bart12atr, bodyt12atr)

        self.signalDf['InsideBar2.' + str(num) +'Long'] = CandleShape.InsideBar2Long(self.chartDf, 
                      bart22atr, bart12atr, bodyt12atr)
        self.signalDf['InsideBar2.' + str(num) +'Short'] = CandleShape.InsideBar2Short(self.chartDf, 
                      bart22atr, bart12atr, bodyt12atr)
        
        self.chartDf['InsideBar2.' + str(num)] = np.zeros([])
        self.chartDf['InsideBar2.' + str(num)][self.signalDf['InsideBar2.' + str(num) +'Long'] == True] = 1
        self.chartDf['InsideBar2.' + str(num)][self.signalDf['InsideBar2.' + str(num) +'Short'] == True] = -1
        
        self.signalNum['InsideBar'][2] += 1

    def AddPureInsideBar(self):
        '''
        Add singal PureInsideBar, T bar is inside T-1 bar
        '''
        self.chartDf = self.chartDf.sort_index()

        self.chartDf['InsideBarPure'] = CandleShape.PureInsideBar(self.chartDf)
        
        
    def AddCombInsideBar(self, bar2atr):
        '''
        Add trading singal InsideBar2
        '''
        self.chartDf = self.chartDf.sort_index()
        
        num = self.signalNum['InsideBarComb'][0]
        self.signalPara['InsideBarComb0.' + str(num)] = (bar2atr)

        self.signalDf['InsideBarComb0.' + str(num) +'Long'] = CandleShape.BreakoutLong(self.chartDf, 
                      bar2atr)
        self.signalDf['InsideBarComb0.' + str(num) +'Short'] = CandleShape.BreakoutShort(self.chartDf, 
                      bar2atr)
        
        self.chartDf['InsideBarComb0.' + str(num)] = self.signalDf['InsideBarComb0.' + str(num) +'Short'] \
                     + self.signalDf['InsideBarComb0.' + str(num) +'Long']
                                     
        copy = self.chartDf['InsideBarComb0.' + str(num)].copy()
        self.chartDf['InsideBarComb0.' + str(num)][(copy <= 1) & (copy >= -1)] = 0
                                     
        self.signalNum['InsideBarComb'][0] += 1
                    
    def _validateBarPeriod(self, period):
        if(type(period) != str):
            return 'Unknown'
        elif(period.lower() == 'year'):
            return 'Year'
        elif(period.lower() == 'month'):
            return 'Month'
        elif(period.lower() == 'week'):
            return 'Week'
        elif(period.lower() == 'day'):
            return 'Day'
        elif(period.lower() == 'minute'):
            return 'Minute'
        else:
            return 'Unknown'