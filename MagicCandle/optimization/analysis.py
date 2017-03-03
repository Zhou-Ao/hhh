# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 16:37:06 2017

@author: strategy.intern.2
"""

import pandas as pd
import numpy as np
import os
import datetime

class CandleAnalysis:
    
    @staticmethod
    def GetBacktestFileNames(path):
        fileNames = []
        for fileName in os.listdir(path):
            if fileName.endswith('.txt'):
                fileNames.append(os.path.join(path, fileName))
                
    @staticmethod            
    def InterpretBacktestResult(fileNames):
        result_df = pd.DataFrame(columns = ['Curncy', 'Signal', 'Parameters', 'HoldingPeriod', 'Period', 
                                            'TotalHits', 'TotalWins', 'HitRate', 'CumReturn',
                                            'MaxReturn', 'AveDrawdown', 'MaxDrawdown'])
        
        # interpret the backtest reuslt files
        for fileName in fileNames:
            print(fileName)
            with open(fileName, 'r') as f:
                for line in f.readlines():
                    if 'Curncy' in line:
                        curncy = line[:6]
                        period = line[-25:-1]
                    elif 'Holding Period:' in line:
                        holdingPeriod  = int(line[16:-1])
                    elif 'Signal:' in line:
                        signal = line[8:-1]
                    elif 'Parameter:' in line:
                        para = line[11:-1]
                    elif 'Total Hits:' in line:
                        hits = int(line[12:-1])
                    elif 'Total Wins:' in line:
                        wins = int(line[12:-1])
                    elif 'Hit Rate: 0.0Cum Return: 0.0' in line:
                        hitRate = 0.0
                        cumReturn = 0.0
                    elif 'Hit Rate:' in line:
                        hitRate = float(line[10:-1])
                    elif 'Cum Return:' in line:
                        cumReturn = float(line[12:-1])
                    elif 'Max Return:' in line:
                        maxReturn = float(line[12:-1])
                    elif 'Average Drawdown:' in line:
                        aveDrawdown = float(line[17:])
                    elif 'Max Drawdown:' in line:
                        maxDrawdown = float(line[14:])
                    elif line == '\n':
                        temp_df = pd.DataFrame({
                                                'Curncy' : curncy,
                                                'Signal' : signal,
                                                'Parameters' : para,
                                                'HoldingPeriod' : holdingPeriod,
                                                'Period' : period,
                                                'TotalHits' : hits,
                                                'TotalWins' : wins,
                                                'HitRate' : hitRate,
                                                'CumReturn' : cumReturn,
                                                'MaxReturn' : maxReturn,
                                                'AveDrawdown' : aveDrawdown,
                                                'MaxDrawdown' : maxDrawdown},
                                                index = [0])
                        
                        result_df = result_df.append(temp_df, ignore_index=True)
        return result_df
      
    @staticmethod
    def FilterByHitRate(df, threshold, minPeriod):
        df_group = df.groupby(['Curncy', 'Signal'])
        # filter by hitrate
        df_filter_group = df_group.filter(lambda x: len(x[x.HitRate > threshold]) >= minPeriod)
        df_filter_df = df.iloc[df_filter_group.index]
    
        return df_filter_df