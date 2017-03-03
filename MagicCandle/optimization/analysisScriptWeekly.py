# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 14:00:58 2017

@author: strategy.intern.2
"""

import pandas as pd
import numpy as np
import os
import datetime

from analysis import CandleAnalysis
#from utlity.utlity import CandleUtility

#------------------------------------------------------------------------------
# Initailize settings
#------------------------------------------------------------------------------

#curncyList = CandleUtility.GetCurncyList()
              
#periodDict = {'t_full' : '2009-09-16 to 2017-02-06',
#              't_2' : '2009-09-16 to 2012-12-31',
#              't_1' : '2013-01-01 to 2015-12-31',
#              't' : '2016-01-01 to 2017-02-06'}
#                
#numOfDays = {'t_full' : (datetime.date(2017,2,6) - datetime.date(2009, 9, 16)).days,
#             't_2' : (datetime.date(2012,12,31) - datetime.date(2009, 9, 16)).days,
#             't_1' : (datetime.date(2015,12,31) - datetime.date(2013, 1, 1)).days,
#             't' : (datetime.date(2017,2,6) - datetime.date(2016, 1, 1)).days}

periodDict = {'t_full' : '2009-01-01 to 2017-02-06',
              't_2' : '2009-01-01 to 2012-01-01',
              't_1' : '2012-01-01 to 2015-01-01',
              't' : '2015-01-01 to 2017-02-06'}
                
numOfDays = {'t_full' : (datetime.date(2017,2,6) - datetime.date(2009, 1, 1)).days,
             't_2' : (datetime.date(2012,1,1) - datetime.date(2009, 1, 1)).days,
             't_1' : (datetime.date(2015,1,1) - datetime.date(2012, 1, 1)).days,
             't' : (datetime.date(2017,2,6) - datetime.date(2015, 1, 1)).days}
              
#------------------------------------------------------------------------------
# Read backtest result from files
#------------------------------------------------------------------------------
#fileNames = CandleAnalysis.GetBacktestFileNames(os.getcwd())
#result_df = CandleAnalysis.InterpretBacktestResult(fileNames)
#filter_df = CandleAnalysis.FilterByHitRate(result_df, 0.55, 4)

#------------------------------------------------------------------------------
# Read Backtest result from HDF store
#------------------------------------------------------------------------------
result_df = {}
filtered_df = {}

store = pd.HDFStore('WeeklyBacktest20170224.h5')
result_df[1] = store['weekly']
store.close()


#store = pd.HDFStore('InsideBarCombBacktest20170220.h5')
#result_df[2] = store['weekly']
#store.close()


#store = pd.HDFStore('insidebarcomb.h5')
#result_df[3] = store['insidebarcomb']
#store.close()
#
#filtered_df[3] = CandleAnalysis.FilterByHitRate(result_df[3], 0.55, 4)

# concate data frame
concate_df = pd.concat([df for df in result_df.itervalues()], ignore_index = True)

#------------------------------------------------------------------------------
# Filter Signal Parameters
#------------------------------------------------------------------------------
# first filter
final_df = CandleAnalysis.FilterByHitRate(concate_df, 0.501, 4)

# second filter
group = final_df.groupby(['Curncy', 'Signal'])
final_df = group.filter(lambda x: len(x[(x.Period==periodDict['t_full']) & (x.CumReturn > 0)]) == 2)

# third filter
group = final_df.groupby(['Curncy', 'Signal'])
final_df = group.filter(lambda x: np.mean(x.HitRate[x.Period==periodDict['t']]) > 0.5)

#------------------------------------------------------------------------------
# Save and Export Result
#------------------------------------------------------------------------------

# export backtest result summary
final_df.groupby(['Curncy', 'Signal', 'Parameters', 'HoldingPeriod', 
                   'Period', 'HitRate', 'TotalHits', 'CumReturn', 
                   'MaxDrawdown']).sum().to_excel('WeeklySummary' + datetime.date.today().strftime('%Y%m%d') + '.xlsx')

# save signals
store = pd.HDFStore('WeeklySignal' + datetime.date.today().strftime('%Y%m%d') + '.h5')
store['signal'] = final_df[final_df.Period == periodDict['t']].groupby(['Curncy', 'Signal', 'Parameters']).mean().reset_index()[['Curncy', 'Signal', 'Parameters', 'HitRate']] 
store.close()
          
# export result by curncy
for curncy in set(final_df.Curncy):
    print(curncy)
    curncy_df = final_df[final_df.Curncy == curncy]
    temp_df = curncy_df.groupby(['Curncy', 'Signal', 'Parameters', 'HoldingPeriod', 
                                 'Period', 'HitRate', 'TotalHits', 'CumReturn', 'MaxDrawdown']).sum()
    
    excel = os.path.join(os.getcwd(), 'Weekly', 'By Currency', curncy+'.xlsx')
    if not os.path.exists(os.path.dirname(excel)):
        os.makedirs(os.path.dirname(excel))
    temp_df.to_excel(excel)


signalList = ['Engulf0', 'InsideBar0', 'Hammer4', 'InsideBarComb0']
    
# export result by signal
for curncy in set(final_df.Curncy):
    for signal in signalList:
        print(curncy + ":" + signal)
        curncy_df = final_df[final_df.Curncy == curncy]
        signalIndex = np.array([signal in sig for sig in final_df[final_df.Curncy == curncy].Signal])
        if signalIndex.any() == True:
            curncy_df = curncy_df[signalIndex]
            temp_df = curncy_df.groupby(['Curncy', 'Signal', 'Parameters', 'HoldingPeriod', 
                                 'Period', 'HitRate', 'TotalHits', 'CumReturn', 'MaxDrawdown']).sum()
            
            excel = os.path.join(os.getcwd(), 'Weekly', 'By Signal' ,signal, curncy+'.xlsx')
            if not os.path.exists(os.path.dirname(excel)):
                os.makedirs(os.path.dirname(excel))
            temp_df.to_excel(excel)

# print count
count_df = pd.DataFrame(columns = ['Curncy', 'Signal', 'Count'])
for curncy in set(final_df.Curncy):
    for signal in signalList:
        curncy_df = final_df[final_df.Curncy == curncy]
        signalIndex = np.array([signal in sig for sig in final_df[final_df.Curncy == curncy].Signal])
        if signalIndex.any() == True:
            curncy_df = curncy_df[signalIndex]
            temp_df = pd.DataFrame({'Curncy' : curncy,
                                    'Signal' : signal,
                                    'Count' : len(curncy_df)/8.0}, index = [0])
            count_df = count_df.append(temp_df, ignore_index = True)
            print(curncy + "," + signal + "," + str(len(curncy_df)/8.0))

count_df.groupby(['Curncy', 'Signal']).sum().to_excel('WeeklyCount' + datetime.date.today().strftime('%Y%m%d') + '.xlsx')