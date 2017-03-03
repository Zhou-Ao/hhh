# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 14:43:43 2017

@author: strategy.intern.2
"""
import numpy as np

class CandleUtility:
    
    @staticmethod
    def GetArrayT(inputList, T):
        if type(T) != int:
            raise Exception('Please insert a int for time length!')
        if T > 0:
            return np.array(inputList[T:] + [np.nan] * T)
        elif T < 0:
            return np.array([np.nan] * (-T) + inputList[:T])
        else:
            return np.array(inputList)
            
    @staticmethod
    def GetTickerList():
#        return ["AUDCAD BGN Curncy", "AUDCHF BGN Curncy", "AUDJPY BGN Curncy", 
#              "AUDNZD BGN Curncy", "AUDUSD BGN Curncy", "CADCHF BGN Curncy",
#              "CADJPY BGN Curncy", "CHFJPY BGN Curncy", "EURAUD BGN Curncy", 
#              "EURCAD BGN Curncy", "EURCHF BGN Curncy", "EURGBP BGN Curncy",
#              "EURJPY BGN Curncy", "EURNZD BGN Curncy", "EURUSD BGN Curncy", 
#              "GBPAUD BGN Curncy", "GBPCAD BGN Curncy", "GBPCHF BGN Curncy",
#              "GBPJPY BGN Curncy", "GBPNZD BGN Curncy", "GBPUSD BGN Curncy", 
#              "NZDCAD BGN Curncy", "NZDCHF BGN Curncy", "NZDJPY BGN Curncy",
#              "NZDUSD BGN Curncy", "USDCAD BGN Curncy", "USDCHF BGN Curncy", 
#              "USDCNH BGN Curncy", "USDJPY BGN Curncy", "USDSGD BGN Curncy",
#              "XAUUSD BGN Curncy"]
              
        return ["AUDUSD Curncy",
                "GBPUSD Curncy",
                "EURUSD Curncy",
                "NZDUSD Curncy",
                "USDCAD Curncy",
                "USDCHF Curncy",
                "USDJPY Curncy",
                "XAUUSD Curncy",
                "USDCNH Curncy",
                "USDSGD Curncy",
                "USDTHB Curncy",
                "AUDJPY Curncy",
                "EURJPY Curncy",
                "GBPJPY Curncy",
                "NZDJPY Curncy",
                "CADJPY Curncy",
                "EURAUD Curncy",
                "EURCAD Curncy",
                "EURCHF Curncy",
                "EURGBP Curncy",
                "GBPAUD Curncy",
                "AUDCAD Curncy",
                "AUDNZD Curncy",
                "EURNZD Curncy",
                "GBPNZD Curncy",
                "GBPCAD Curncy",
                "NZDCAD Curncy",
                "GBPCHF Curncy",
                "CCN+1M Curncy",
                "IHN+1M Curncy",
                "IRN+1M Curncy",
                "KWN+1M Curncy",
                "MRN+1M Curncy",
                "NTN+1M Curncy",
                "PPN+1M Curncy",
                "TY1 COMDTY",
                "ES1 INDEX",
                "NH1 INDEX"]
              
#    @staticmethod
#    def GetCurncyList():
#        return ["AUDCAD", "AUDCHF", "AUDJPY", "AUDNZD", "AUDUSD", "CADCHF",
#              "CADJPY", "CHFJPY", "EURAUD", "EURCAD", "EURCHF", "EURGBP",
#              "EURJPY", "EURNZD", "EURUSD", "GBPAUD", "GBPCAD", "GBPCHF",
#              "GBPJPY", "GBPNZD", "GBPUSD", "NZDCAD", "NZDCHF", "NZDJPY",
#              "NZDUSD", "USDCAD", "USDCHF", "USDCNH", "USDJPY", "USDSGD",
#              "XAUUSD"]