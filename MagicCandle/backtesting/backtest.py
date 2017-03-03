# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 13:47:11 2017

@author: strategy.intern.2
"""
import pandas as pd
import numpy as np
import tia.bbg.datamgr as dm
from utility.utility import CandleUtility

class CandleBacktester:
    
    def __init__(self, ticker, startDate, endDate, freq):
        self.ticker = ticker
        self.startDate = startDate
        self.endDate = endDate
        self.freq = freq
        
        # retrieve data from blp
        self._mgr = dm.BbgDataManager()
        self._symbol = self._mgr[ticker]
        if freq == 'Daily':
            self._blp_df = self._symbol.get_historical(['PX_LAST'], startDate.strftime('%m/%d/%Y'), endDate.strftime('%m/%d/%Y'))
        elif freq == 'Weekly':
            self._blp_df = self._symbol.get_historical(['PX_LAST'], startDate.strftime('%m/%d/%Y'), endDate.strftime('%m/%d/%Y'),
                                                       period='WEEKLY')
        else:
            raise Exception('CandleBacktester: Invalid backtest frenquency! Daily or Weekly')
            
    def Backtest(self, signalList, chartDf, signalParaDict, holdingPeriod):
        # check signal column in signalDf
        if not (set(signalList).issubset(chartDf.columns)):
            raise Exception('CandleBacktester: Invalid dataframe!')
        
        result_df = pd.DataFrame(columns = ['Curncy', 'Signal', 'Parameters', 'Frequency', 'HoldingPeriod', 'Period', 
                                        'TotalHits', 'TotalWins', 'HitRate', 'CumReturn',
                                        'MaxReturn', 'AveDrawdown', 'MaxDrawdown'])
            
        # sort datetime index
        signalDf = chartDf.sort_index()
        signalDf = signalDf.loc[self.startDate:self.endDate, signalList]
        
        # create backtest dataframe
        backtest_df = pd.DataFrame(self._blp_df.iloc[:,0].tolist(), columns=['Last'], index = self._blp_df.index)
        # exit price
        backtest_df['LastAfter'] = CandleUtility.GetArrayT(backtest_df.Last.tolist(), holdingPeriod)
        # daily return
        backtest_df['Return'] = backtest_df.LastAfter / backtest_df.Last - 1
        # concat signals to df
        backtest_df = pd.concat([backtest_df, signalDf[signalList]], axis=1)
        # calculate signal returns
        returnMatrix = np.array(backtest_df.Return).reshape(len(backtest_df.Return), 1) \
            * np.true_divide(np.array(backtest_df[signalList]), np.abs(np.array(backtest_df[signalList])))
        returnMatrix[np.isnan(returnMatrix)] = 0
        returnMatrix[np.isinf(returnMatrix)] = 0
        strategy_df = pd.DataFrame(returnMatrix,
                                   columns = [signal + 'Return' for signal in signalList],
                                    index = backtest_df.index)
        
        backtest_df = pd.concat([backtest_df, strategy_df], axis=1)
        backtest_df = backtest_df.dropna(how='any')
        
        
#            with open('backtest' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.txt', 'w') as f:
#                f.write('Backtest Summary\n')
#                for signal in signalList:
#                    f.write(self.ticker + ' from ' + self.startTime.strftime('%Y-%m-%d') + ' to ' + self.endTime.strftime('%Y-%m-%d') + '\n')
#                    f.write('Holding Period: ' + str(holdingPeriod) + '\n')
#                    f.write('Signal: ' + signal + '\n')
#                    f.write('Parameter: ' + str(signalParaDict[signal]) + '\n')
#                    f.write('Total Hits: ' + str(len(backtest_df[backtest_df[signal] != 0])) + '\n')
#                    f.write('Total Wins: ' + str(len(backtest_df[backtest_df[signal + 'Return']> 0])) + '\n')
#                    if len(backtest_df[backtest_df[signal] != 0]) == 0:
#                        f.write('Hit Rate: 0.0\n')
#                    else:
#                        f.write('Hit Rate: ' + str(1.0*len(backtest_df[backtest_df[signal + 'Return']> 0]) / len(backtest_df[backtest_df[signal] != 0])) + '\n')
#                    f.write('Cum Return: ' + str(np.prod(1 + backtest_df[signal + 'Return']) - 1) + '\n')
#                    f.write('Max Return: ' + str(np.max(backtest_df[signal + 'Return'])) + '\n')
#                    f.write('Average Drawdown:' + str(np.mean(backtest_df[signal + 'Return'][backtest_df[signal + 'Return']< 0])) + '\n')
#                    f.write('Max Drawdown: ' + str(np.min(backtest_df[signal + 'Return'])) + '\n')
#                    f.write('\n')
#            return backtest_df
            
        # summarize signal performance 
        for signal in signalList:
            temp_df = pd.DataFrame({
                                    'Curncy' : self.ticker,
                                    'Signal' : signal,
                                    'Parameters' : str(signalParaDict[signal]),
                                    'Frequency' : self.freq,
                                    'HoldingPeriod' : holdingPeriod,
                                    'Period' : self.startDate.strftime('%Y-%m-%d') + ' to ' + self.endDate.strftime('%Y-%m-%d'),
                                    'TotalHits' : len(backtest_df[backtest_df[signal] != 0]),
                                    'TotalWins' : len(backtest_df[backtest_df[signal + 'Return']> 0]),
                                    'HitRate' : 0.0 if len(backtest_df[backtest_df[signal] != 0]) == 0 \
                                                    else 1.0*len(backtest_df[backtest_df[signal + 'Return']> 0]) / len(backtest_df[backtest_df[signal] != 0]),
                                    'CumReturn' : np.prod(1 + backtest_df[signal + 'Return']) - 1,
                                    'MaxReturn' : np.max(backtest_df[signal + 'Return']),
                                    'AveDrawdown' : np.mean(backtest_df[signal + 'Return'][backtest_df[signal + 'Return']< 0]),
                                    'MaxDrawdown' : np.min(backtest_df[signal + 'Return'])
                                    }, index = [0])
            
            result_df = result_df.append(temp_df, ignore_index=True)
                
        return result_df