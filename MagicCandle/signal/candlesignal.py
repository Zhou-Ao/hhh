# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 13:35:08 2017

@author: strategy.intern.2
"""
import numpy as np
import pandas as pd

import datetime

class CandleSignal:
    @staticmethod
    def GetFloatPattern():
        return '[-+]?[0-9]*\\.?[0-9]+' # float
        
    @staticmethod
    def AggregateRowSignals(row):
        if (row == 1).any() and (row == -1).any():
            # conflict signal
            return 9981
        elif (row == 1).any():
            # buy signal
            return 1.0
        elif (row == -1).any():
            # sell signal
            return -1.0
        else:
            return 0.0
        
    @staticmethod
    def Signal2Str(signal):
        if signal > 0:
            return 'BUY'
        elif signal < 0:
            return 'SELL'
        else:
            return 'UNKNOWN'
            
    @staticmethod
    def AddSignals(ticker, chart, signalDf):
        for row in signalDf[signalDf.Curncy == ticker].itertuples(index = False):
            print(row)
            # row: Curncy, Signal, Parameters
            paraList = [float(para) for para in row[2]]
            if 'Engulf1' in row[1]:
                chart.AddEngulf1(paraList[0], paraList[1])
            elif 'Engulf2' in row[1]:
                chart.AddEngulf2(paraList[0], paraList[1])
            elif 'Engulf0' in row[1]:
                chart.AddEngulf(paraList[0], paraList[1])
            elif 'InsideBar1' in row[1]:
                chart.AddInsideBar1(paraList[0])
            elif 'InsideBar2' in row[1]:
                chart.AddInsideBar2(paraList[0], paraList[1], paraList[2])
            elif 'InsideBar0' in row[1]:
                chart.AddInsideBar(paraList[0], paraList[1])
            elif 'Hammer4' in row[1]:
                chart.AddHammer4(paraList[0], paraList[1], paraList[2], paraList[3])
            elif 'InsideBarComb0' in row[1]:
                chart.AddPureInsideBar()
                chart.AddCombInsideBar(paraList[0])
            else:
                print('Warning: Unkown signal!')
                
    @staticmethod
    def AggregateSignals(ticker, chart, signalDf):
        engulfCol = [('Engulf0' in col) or ('Engulf1' in col) or ('Engulf2' in col) for col in chart.chartDf.columns]
        chart.chartDf['Engulf'] = chart.chartDf.iloc[:, engulfCol].apply(CandleSignal.AggregateRowSignals, axis = 1)
        engulfSignalRow = ['Engulf' in col for col in signalDf[signalDf.Curncy == ticker]['Signal']]
        if engulfSignalRow != []:
            hitrate = np.array(signalDf[signalDf.Curncy == ticker][engulfSignalRow]['HitRate'])
            if np.array(chart.chartDf.iloc[:, engulfCol]).shape[1] > 0:
                conviction = np.array(chart.chartDf.iloc[:, engulfCol]) * hitrate
                chart.chartDf['EngulfConviction'] \
                    = np.abs(np.true_divide(conviction.sum(1),(conviction!=0).sum(1)))
        
        InsideBarCol = [('InsideBar0' in col) or ('InsideBar1' in col) or ('InsideBar2' in col) for col in chart.chartDf.columns]
        chart.chartDf['InsideBar'] = chart.chartDf.iloc[:, InsideBarCol].apply(CandleSignal.AggregateRowSignals, axis = 1)
        insideBarSignalRow = [(('InsideBar' in col) and ('InsideBarComb' not in col)) for col in signalDf[signalDf.Curncy == ticker]['Signal']]
        if insideBarSignalRow != []:
            hitrate = np.array(signalDf[signalDf.Curncy == ticker][insideBarSignalRow]['HitRate'])
            if np.array(chart.chartDf.iloc[:, InsideBarCol]).shape[1] > 0:
                conviction = np.array(chart.chartDf.iloc[:, InsideBarCol]) * hitrate
                chart.chartDf['InsideBarConviction'] \
                    = np.abs(np.true_divide(conviction.sum(1),(conviction!=0).sum(1)))
        
        HammerCol = [('Hammer4' in col) or ('Hammer1' in col) or ('Hammer2' in col) or ('Hammer3' in col) for col in chart.chartDf.columns]
        chart.chartDf['Hammer'] = chart.chartDf.iloc[:, HammerCol].apply(CandleSignal.AggregateRowSignals, axis = 1)
        hammerSignalRow = ['Hammer' in col for col in signalDf[signalDf.Curncy == ticker]['Signal']]
        if hammerSignalRow != []:
            hitrate = np.array(signalDf[signalDf.Curncy == ticker][hammerSignalRow]['HitRate'])
            if np.array(chart.chartDf.iloc[:, HammerCol]).shape[1] > 0:
                conviction = np.array(chart.chartDf.iloc[:, HammerCol]) * hitrate
                chart.chartDf['HammerConviction'] \
                    = np.abs(np.true_divide(conviction.sum(1),(conviction!=0).sum(1)))
                    
        InsideBarCombCol = [('InsideBarComb0' in col) for col in chart.chartDf.columns]
        chart.chartDf['InsideBarComb'] = chart.chartDf.iloc[:, InsideBarCombCol].apply(CandleSignal.AggregateRowSignals, axis = 1)
        insideBarCombSignalRow = ['InsideBarComb' in col for col in signalDf[signalDf.Curncy == ticker]['Signal']]
        if insideBarCombSignalRow != []:
            hitrate = np.array(signalDf[signalDf.Curncy == ticker][insideBarCombSignalRow]['HitRate'])
            if np.array(chart.chartDf.iloc[:, InsideBarCombCol]).shape[1] > 0:
                conviction = np.array(chart.chartDf.iloc[:, InsideBarCombCol]) * hitrate
                chart.chartDf['InsideBarCombConviction'] \
                    = np.abs(np.true_divide(conviction.sum(1),(conviction!=0).sum(1)))
        
        chart.chartDf = chart.chartDf.dropna(axis = 1, how = 'all')
        
    @staticmethod
    def CreateSummaryDf(signal, ticker, chart, date):
        if (signal in chart.chartDf.columns) and (chart.chartDf[signal].loc[date] != 0):
            temp_df = pd.DataFrame({'CCY' : ticker,
                                    'SIGNAL' : CandleSignal.Signal2Str(chart.chartDf[signal].loc[date]),
                                    'CONVICTION' : chart.chartDf[signal + 'Conviction'].loc[date],
                                    'TYPE' : signal.upper()},
                               index = [date])
            return temp_df
            
    @staticmethod
    def CreateSimpleSummaryDf(signal, ticker, chart, date):
        if (signal in chart.chartDf.columns) and (chart.chartDf[signal].loc[date] != 0):
            temp_df = pd.DataFrame({'CCY' : ticker,
                                    'SIGNAL' : CandleSignal.Signal2Str(chart.chartDf[signal].loc[date]),
                                    'TYPE' : signal.upper()},
                               index = [date])
            return temp_df
            
    @staticmethod
    def AddDateColumn(df, freq):
        if freq == 'Daily': 
            df['Date'] = map(lambda x: 'Today' if np.ceil((datetime.datetime.today() - x).days / 1.0) - 1 == 0
                                else str(int(np.ceil((datetime.datetime.today() - x).days / 1.0) - 1)) + ' day(s) ago', 
                                df.index)
        elif freq == 'Weekly':
            df['Date'] = map(lambda x: 'This week' if np.ceil((datetime.datetime.today() - x).days / 7.0) - 1 == 0
                                else str(int(np.ceil((datetime.datetime.today() - x).days / 7.0) - 1)) + ' week(s) ago',
                                df.index)
        
        