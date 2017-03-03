# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 15:14:44 2017

@author: Ao
"""
import numpy as np
from utility.utility import CandleUtility

class CandleShape:
    
    
    @staticmethod
    def HammerLong(df, bar2atr, body2atr, lowershadow2atr_1, lowershadow2uppershadow, 
                    uppdershadow2body, uppershadow2lowershadow_2, lowershadow2bar_2,
                    lowershadowplusbody2atr, lowershadow2atr_3, uppershadow2bar, uppershadow2lowershadow_3, lowershadow2bar_3):
        return CandleShape.Hammer1Long(df, bar2atr, body2atr, lowershadow2atr_1, lowershadow2uppershadow, 
                    uppdershadow2body) \
                | CandleShape.Hammer2Long(df, bar2atr, uppershadow2lowershadow_2, lowershadow2bar_2,
                    lowershadowplusbody2atr) \
                | CandleShape.Hammer3Long(df, bar2atr, lowershadow2atr_3, uppershadow2bar, 
                    uppershadow2lowershadow_3, lowershadow2bar_3)
                
    @staticmethod
    def HammerShort(df, bar2atr, body2atr, uppershadow2atr_1, uppershadow2lowershadow, 
                     lowershadow2body, lowershadow2uppershadow_2, uppershadow2bar_2,
                    uppershadowplusbody2atr, uppershadow2atr_3, lowershadow2bar, lowershadow2uppershadow_3, uppershadow2bar_3):
        return CandleShape.Hammer1Short(df, bar2atr, body2atr, uppershadow2atr_1, uppershadow2lowershadow, 
                     lowershadow2body) \
                | CandleShape.Hammer2Short(df, bar2atr, lowershadow2uppershadow_2, uppershadow2bar_2,
                    uppershadowplusbody2atr) \
                | CandleShape.Hammer3Short(df, bar2atr, uppershadow2atr_3, lowershadow2bar, 
                    lowershadow2uppershadow_3, uppershadow2bar_3)
    
    
    # Hammer 1
    # Rules (Long)
    # 1.       Bar > 0.7*ATR
    # 2.       Open <= Average (Prev 3 Opens)
    # 3.       Body > 0.38*ATR
    # 4.       Lower Shadow > 0.28*ATR
    # 5.       Lower Shadow > 2* Upper Shadow
    # 6.       Upper Shadow < 0.35 * Body
    # 7.       Must be White Bar
    @staticmethod
    def Hammer1Long(df, bar2atr, body2atr, lowershadow2atr, lowershadow2uppershadow, 
                    uppdershadow2body):
        if set(['BarToATR', 'Open', 'BodyToATR', 'LowerShadowToATR',
                'LowerShadowToUpperShadow', 'UpperShadowToBody', 'Close']).issubset(df.columns):
                logic1 = np.array(df.BarToATR) > bar2atr
                logic2 = np.array(df.Open) <= np.array(df.Open.rolling(window=4).apply(lambda x: np.mean(x[:-1])))
                logic3 = np.array(df.BodyToATR) > body2atr
                logic4 = np.array(df.LowerShadowToATR) > lowershadow2atr
                logic5 = np.array(df.LowerShadowToUpperShadow) > lowershadow2uppershadow
                logic6 = np.array(df.UpperShadowToBody) < uppdershadow2body
                logic7 = np.array(df.Close) > np.array(df.Open) # white bar
                                 
                return logic1 & logic2 & logic3 & logic4 & logic5 & logic6 & logic7
            
        else:
            raise Exception('CandleShape: Invalid dataframe!')
    
    # Hammer1
    # Rules (Short)
    # 1.       Bar > 0.7*ATR
    # 2.       Open >= Average (Prev 3 Opens)
    # 3.       Body > 0.38*ATR
    # 4.       Upper Shadow > 0.28*ATR
    # 5.       Upper Shadow > 2* Lower Shadow
    # 6.       Lower Shadow < 0.35 * Body
    # 7.       Must be Filled Bar
    @staticmethod
    def Hammer1Short(df, bar2atr, body2atr, uppershadow2atr, uppershadow2lowershadow, 
                     lowershadow2body):
        if set(['BarToATR', 'Open', 'BodyToATR', 'LowerShadowToATR', 
            'LowerShadowToUpperShadow', 'UpperShadowToBody', 'Close']).issubset(df.columns):
                logic1 = np.array(df.BarToATR) > bar2atr
                logic2 = np.array(df.Open) >= np.array(df.Open.rolling(window=4).apply(lambda x: np.mean(x[:-1])))
                logic3 = np.array(df.BodyToATR) > body2atr
                logic4 = np.array(df.UpperShadowToATR) > uppershadow2atr
                logic5 = np.array(df.UpperShadowToLowerShadow) > uppershadow2lowershadow
                logic6 = np.array(df.LowerShadowToBody) < lowershadow2body
                logic7 = np.array(df.Close) < np.array(df.Open) # filled bar
                                 
                return logic1 & logic2 & logic3 & logic4 & logic5 & logic6 & logic7
            
        else:
            raise Exception('CandleShape: Invalid dataframe!')

    # Hammer 2
    # Rules (Long)
    # 1.       Bar > 0.7*ATR
    # 2.       Open <= Average (Prev 3 Opens)
    # 3.       Upper shadow < 0.44 *Lower shadow
    # 4.       Lower shadow > 0.55 *Bar
    # 5.       Lower Shadow + Body > 0.7* ATR
    # 6.       Must be White Bar
    @staticmethod   
    def Hammer2Long(df, bar2atr, uppershadow2lowershadow, lowershadow2bar,
                    lowershadowplusbody2atr):
        if set(['BarToATR', 'Open', 'UpperShadowToLowerShadow', 'LowerShadowToBar',
            'LowerShadowToATR', 'BodyToATR', 'Close']).issubset(df.columns):
                logic1 = np.array(df.BarToATR) > bar2atr
                logic2 = np.array(df.Open) <= np.array(df.Open.rolling(window=4).apply(lambda x: np.mean(x[:-1])))
                logic3 = np.array(df.UpperShadowToLowerShadow) < uppershadow2lowershadow
                logic4 = np.array(df.LowerShadowToBar) > lowershadow2bar
                logic5 = (np.array(df.LowerShadowToATR) + np.array(df.BodyToATR)) > lowershadowplusbody2atr
                logic6 = np.array(df.Close) > np.array(df.Open) # white bar
                
                return logic1 & logic2 & logic3 & logic4 & logic5 & logic6
        else:
            raise Exception('CandleShape: Invalid dataframe!')

    # Hammer2
    # Rules (Short)
    # 1.       Bar > 0.7*ATR
    # 2.       Open >= Average (Prev 3 Opens)
    # 3.       Lower shadow < 0.44 *Upper shadow
    # 4.       Upper shadow > 0.55 *Bar
    # 5.       Upper Shadow + Body > 0.7* ATR
    # 6.       Must be Filled Bar
    @staticmethod
    def Hammer2Short(df, bar2atr, lowershadow2uppershadow, uppershadow2bar,
                    uppershadowplusbody2atr):
        if set(['BarToATR', 'Open', 'LowerShadowToUpperShadow', 'UpperShadowToBar', 
            'UpperShadowToATR', 'BodyToATR', 'Close']).issubset(df.columns):
                logic1 = np.array(df.BarToATR) > bar2atr
                logic2 = np.array(df.Open) >= np.array(df.Open.rolling(window=4).apply(lambda x: np.mean(x[:-1])))
                logic3 = np.array(df.LowerShadowToUpperShadow) < lowershadow2uppershadow
                logic4 = np.array(df.UpperShadowToBar) > uppershadow2bar
                logic5 = (np.array(df.UpperShadowToATR) + np.array(df.BodyToATR)) > uppershadowplusbody2atr
                logic6 = np.array(df.Close) < np.array(df.Open) # filled bar
                
                return logic1 & logic2 & logic3 & logic4 & logic5 & logic6
        else:
            raise Exception('CandleShape: Invalid dataframe!')
    
    # Hammer 3
    # Rules (Long)
    # 1.       Bar > 0.7*ATR
    # 2.       Open <= Average (Prev 3 Opens)
    # 3.       Lower Shadow >= 0.5*ATR
    # 4.       Upper shadow < 0.15 *Bar
    # 5.       Upper shadow < 0.2* Lower
    # 6.       Lower shadow > 0.7*Bar
    @staticmethod
    def Hammer3Long(df, bar2atr, lowershadow2atr, uppershadow2bar, 
                    uppershadow2lowershadow, lowershadow2bar):
        if set(['BarToATR', 'Open', 'Close', 'LowerShadowToATR', 'UpperShadowToBar', 
            'UpperShadowToLowerShadow', 'LowerShadowToBar']).issubset(df.columns):
                logic1 = np.array(df.BarToATR) > bar2atr
                logic2 = np.array(df.Open) <= np.array(df.Open.rolling(window=4).apply(lambda x: np.mean(x[:-1])))
                logic3 = np.array(df.LowerShadowToBar) >= lowershadow2bar
                logic4 = np.array(df.UpperShadowToBar) < uppershadow2bar
                logic5 = np.array(df.UpperShadowToLowerShadow) < uppershadow2lowershadow
                logic6 = np.array(df.LowerShadowToBar) > lowershadow2bar
                
                return logic1 & logic2 & logic3 & logic4 & logic5 & logic6
        else:
            raise Exception('CandleShape: Invalid dataframe!')

    # Hammer3
    # Rules (Short)
    # 1.       Bar > 0.7*ATR
    # 2.       Open >= Average (Prev 3 Opens)
    # 3.       Upper Shadow >= 0.5*ATR
    # 4.       Lower shadow < 0.15 *Bar
    # 5.       Lower shadow < 0.2* Upper 
    # 6.       Upper shadow > 0.7*Bar
    @staticmethod
    def Hammer3Short(df, bar2atr, uppershadow2atr, lowershadow2bar, 
                    lowershadow2uppershadow, uppershadow2bar):
        if set(['BarToATR', 'Open', 'Close', 'LowerShadowToATR', 'UpperShadowToBar', 
            'UpperShadowToLowerShadow', 'LowerShadowToBar']).issubset(df.columns):
                logic1 = np.array(df.BarToATR) > bar2atr
                logic2 = np.array(df.Open) >= np.array(df.Open.rolling(window=4).apply(lambda x: np.mean(x[:-1])))
                logic3 = np.array(df.UpperShadowToBar) >= uppershadow2atr
                logic4 = np.array(df.LowerShadowToBar) < lowershadow2bar
                logic5 = np.array(df.LowerShadowToUpperShadow) < lowershadow2uppershadow
                logic6 = np.array(df.UpperShadowToBar) > uppershadow2bar
                
                return logic1 & logic2 & logic3 & logic4 & logic5 & logic6
        else:
            raise Exception('CandleShape: Invalid dataframe!')
            
        # Hammer 4
    # Rules (Long)
    # 1.       Bar > 0.7*ATR
    # 2.       Open <= Average (Prev 3 Opens)
    # 3.       Body < 0.38*ATR
    # 4.       Lower Shadow > 2.0*ATR
    # 5.       Upper Shadow < 0.1 * ATR
    # 7.       Must be White 
    @staticmethod
    def Hammer4Long(df, bar2atr, body2atr, lowershadow2atr, uppershadow2atr):
        if set(['BarToATR', 'Open', 'BodyToATR', 'UpperShadowToATR',
                'LowerShadowToATR', 'Close']).issubset(df.columns):
#                logic1 = np.array(df.BarToATR) > bar2atr
                logic1 = True
                logic2 = np.array(df.Open) <= np.array(df.Open.rolling(window=4).apply(lambda x: np.mean(x[:-1])))
                logic3 = np.array(df.BodyToATR) < body2atr
                logic4 = np.array(df.LowerShadowToATR) > lowershadow2atr
                logic5 = np.array(df.UpperShadowToATR) < uppershadow2atr
                logic6 = np.array(df.Close) > np.array(df.Open) # white bar
                                 
                return logic1 & logic2 & logic3 & logic4 & logic5 & logic6
            
        else:
            raise Exception('CandleShape: Invalid dataframe!')

    # Hammer 4
    # Rules (Short)
    # 1.       Bar > 0.7*ATR
    # 2.       Open >= Average (Prev 3 Opens)
    # 3.       Body < 0.38*ATR
    # 4.       Lower Shadow > 2.0*ATR
    # 5.       Upper Shadow < 0.1 * ATR
    # 7.       Must be Filled 
    @staticmethod
    def Hammer4Short(df, bar2atr, body2atr, lowershadow2atr, uppershadow2atr):
        if set(['BarToATR', 'Open', 'BodyToATR', 'UpperShadowToATR',
                'LowerShadowToATR', 'Close']).issubset(df.columns):
#                logic1 = np.array(df.BarToATR) > bar2atr
                logic1 = True
                logic2 = np.array(df.Open) >= np.array(df.Open.rolling(window=4).apply(lambda x: np.mean(x[:-1])))
                logic3 = np.array(df.BodyToATR) < body2atr
                logic4 = np.array(df.LowerShadowToATR) > lowershadow2atr
                logic5 = np.array(df.UpperShadowToATR) < uppershadow2atr
                logic6 = np.array(df.Close) < np.array(df.Open) # filled bar
                                 
                return logic1 & logic2 & logic3 & logic4 & logic5 & logic6
            
        else:
            raise Exception('CandleShape: Invalid dataframe!')        
            
    # Engulf 1
    # Rules (Long)
    # 1.       Bar > 1.25*ATR
    # 2.       Body > 0.7*ATR
    # 3.       T = White Bar
    # 4.       T Body > T-1 Body
    # 5.       T Low < T-1 Low
    # 6.       T High > T-1 High
    @staticmethod
    def Engulf1Long(df, bar2atr, body2atr):
        if(set(['BarToATR', 'BodyToATR', 'Body', 'Low', 'High',
            'Open', 'Close']).issubset(df.columns)):
            logic1 = np.array(df.BarToATR) > bar2atr
            logic2 = np.array(df.BodyToATR) > body2atr
            logic3 = np.array(df.Close) > np.array(df.Open) # white bar
            logic4 = np.array(df.Body) > CandleUtility.GetArrayT(df.Body.tolist(), -1)
            logic5 = np.array(df.Low) < CandleUtility.GetArrayT(df.Low.tolist(), -1)
            logic6 = np.array(df.High) > CandleUtility.GetArrayT(df.High.tolist(), -1)

            return logic1 & logic2 & logic3 & logic4 & logic5 & logic6
        else:
            raise Exception('CandleShape: Invalid dataframe!')

    # Engulf1
    # Rules (Short)
    # 1.       Bar > 1.25*ATR
    # 2.       Body > 0.7*ATR
    # 3.       T = Filled Bar
    # 4.       T Body > T-1 Body
    # 5.       T Low < T-1 Low
    # 6.       T High > T-1 High
    @staticmethod
    def Engulf1Short(df, bar2atr, body2atr):
        if(set(['BarToATR', 'BodyToATR', 'Body', 'Low', 'High',
            'Open', 'Close']).issubset(df.columns)):
            logic1 = np.array(df.BarToATR) > bar2atr
            logic2 = np.array(df.BodyToATR) > body2atr
            logic3 = np.array(df.Close) < np.array(df.Open) # filled bar
            logic4 = np.array(df.Body) > CandleUtility.GetArrayT(df.Body.tolist(), -1)
            logic5 = np.array(df.Low) < CandleUtility.GetArrayT(df.Low.tolist(), -1)
            logic6 = np.array(df.High) > CandleUtility.GetArrayT(df.High.tolist(), -1)

            return logic1 & logic2 & logic3 & logic4 & logic5 & logic6
        else:
            raise Exception('CandleShape: Invalid dataframe!')

    # Engulf 2
    # Rules (Long)
    # 1.       Bar > 1.25*ATR
    # 2.       Body > 0.7*ATR
    # 3.       T = White Bar
    # 4.       T Body > T-1 Body
    # 5.       T Close > T-1 Close
    # 6.       T Close > T-2 Close
    # 7.       T High > T-1 High
    # 8.       T High > T-2 High
    @staticmethod
    def Engulf2Long(df, bar2atr, body2atr):
        if(set(['BarToATR', 'BodyToATR', 'Body', 'Low', 'High',
            'Open', 'Close']).issubset(df.columns)):
            logic1 = np.array(df.BarToATR) > bar2atr
            logic2 = np.array(df.BodyToATR) > body2atr
            logic3 = np.array(df.Close) > np.array(df.Open) # white bar
            logic4 = np.array(df.Body) > CandleUtility.GetArrayT(df.Body.tolist(), -1)
            logic5 = np.array(df.Close) > CandleUtility.GetArrayT(df.Close.tolist(), -1)
            logic6 = np.array(df.Close) > CandleUtility.GetArrayT(df.Close.tolist(), -2)
            logic7 = np.array(df.High) > CandleUtility.GetArrayT(df.High.tolist(), -1)
            logic8 = np.array(df.High) > CandleUtility.GetArrayT(df.High.tolist(), -2)

            return logic1 & logic2 & logic3 & logic4 & logic5 & logic6 & logic7 & logic8
        else:
            raise Exception('CandleShape: Invalid dataframe!')

    # Engulf2
    # Rules (Short)
    # 1.       Bar > 1.25*ATR
    # 2.       Body > 0.7*ATR
    # 3.       T = Filled Bar
    # 4.       T Body > T-1 Body
    # 5.       T Close < T-1 Close
    # 6.       T Close < T-2 Close
    # 7.       T Low < T-1 Low
    # 8.       T Low < T-2 Low
    @staticmethod
    def Engulf2Short(df, bar2atr, body2atr):
        if(set(['BarToATR', 'BodyToATR', 'Body', 'Low', 'High',
            'Open', 'Close']).issubset(df.columns)):
            logic1 = np.array(df.BarToATR) > bar2atr
            logic2 = np.array(df.BodyToATR) > body2atr
            logic3 = np.array(df.Close) < np.array(df.Open) # filled bar
            logic4 = np.array(df.Body) > CandleUtility.GetArrayT(df.Body.tolist(), -1)
            logic5 = np.array(df.Close) < CandleUtility.GetArrayT(df.Close.tolist(), -1)
            logic6 = np.array(df.Close) < CandleUtility.GetArrayT(df.Close.tolist(), -2)
            logic7 = np.array(df.Low) < CandleUtility.GetArrayT(df.Low.tolist(), -1)
            logic8 = np.array(df.Low) < CandleUtility.GetArrayT(df.Low.tolist(), -2)

            return logic1 & logic2 & logic3 & logic4 & logic5 & logic6 & logic7 & logic8
        else:
            raise Exception('CandleShape: Invalid dataframe!')
            
    @staticmethod
    def EngulfLong(df, uppershadow2bar, body2atr):
        # upper shadow < 0.1 * bar
        logic1 = np.array(df.UpperShadowToBar) < uppershadow2bar
        # body > 0.8 atr
        logic2 = np.array(df.BodyToATR) > body2atr
        
        # T body > T-1 body
        logic3 = np.array(df.Body) > CandleUtility.GetArrayT(df.Body.tolist(), -1)
        # white bar
        logic4 = np.array(df.Close) > np.array(df.Open) # white bar
        
        # T low < T-1 low
        logic5 = np.array(df.Low) < CandleUtility.GetArrayT(df.Low.tolist(), -1)
        # T high > T-1 high
        logic6 = np.array(df.High) > CandleUtility.GetArrayT(df.High.tolist(), -1)
        
        # T high > T-2 high
        logic7 = np.array(df.High) > CandleUtility.GetArrayT(df.High.tolist(), -2)
        # T close > T-1 close
        logic8 = np.array(df.Close) > CandleUtility.GetArrayT(df.Close.tolist(), -1)
        # T close > T-2 close
        logic9 = np.array(df.Close) > CandleUtility.GetArrayT(df.Close.tolist(), -2)
        # T low < T-1 close
        logic10 = np.array(df.Low) < CandleUtility.GetArrayT(df.Close.tolist(), -1)
        
        return logic1 & logic2 & logic3 & logic4 & \
                    ((logic5 & logic6) | (logic6 & logic7 & logic8 & logic9 & logic10)) 

                    
    @staticmethod
    def EngulfShort(df, lowershadow2bar, body2atr):
        # lower shadow < 0.1 * bar
        logic1 = np.array(df.LowerShadowToBar) < lowershadow2bar
        # body > 0.8 atr
        logic2 = np.array(df.BodyToATR) > body2atr
        
        # T body > T-1 body
        logic3 = np.array(df.Body) > CandleUtility.GetArrayT(df.Body.tolist(), -1)
        # filled bar
        logic4 = np.array(df.Close) < np.array(df.Open) # filled bar
        
        # T low < T-1 low
        logic5 = np.array(df.Low) < CandleUtility.GetArrayT(df.Low.tolist(), -1)
        # T high > T-1 high
        logic6 = np.array(df.High) > CandleUtility.GetArrayT(df.High.tolist(), -1)
        
        # T low < T-2 low
        logic7 = np.array(df.Low) < CandleUtility.GetArrayT(df.Low.tolist(), -2)
        # T close < T-1 close
        logic8 = np.array(df.Close) < CandleUtility.GetArrayT(df.Close.tolist(), -1)
        # T close < T-2 close
        logic9 = np.array(df.Close) < CandleUtility.GetArrayT(df.Close.tolist(), -2)
        # T high > T-1 close
        logic10 = np.array(df.High) > CandleUtility.GetArrayT(df.Close.tolist(), -1)
        
        return logic1 & logic2 & logic3 & logic4 & \
                    ((logic5 & logic6) | (logic5 & logic7 & logic8 & logic9 & logic10)) 

#    @staticmethod
#    def InsideBarLong(df, body2atr_t2, body2atr):
#        # T-2 body > 0.7 T-2 ATR
#        logic1 = CandleUtility.GetArrayT(df.BodyToATR.tolist(), -2) > body2atr_t2
#        # T body > 0.7 T ATR
#        logic2 = np.array(df.BodyToATR) > body2atr
#        # T close > T-2 high
#        logic3 = np.array(df.Close) > CandleUtility.GetArrayT(df.High.tolist(), -2)
#        
#        # T-1 low >= T-2 low
#        logic4 = CandleUtility.GetArrayT(df.Low.tolist(), -1) \
#                >= CandleUtility.GetArrayT(df.Low.tolist(), -2)
#        # T-1 high <= T-2 high
#        logic5 = CandleUtility.GetArrayT(df.High.tolist(), -1) \
#                <= CandleUtility.GetArrayT(df.High.tolist(), -2)
#                
#        # T-1 close > T-2 close
#        logic6 = CandleUtility.GetArrayT(df.Close.tolist(), -1) \
#                > CandleUtility.GetArrayT(df.Close.tolist(), -2) 
#        
#        return logic1 & logic2 & logic3 & ((logic4 & logic5) | (logic5 & logic6))
        
#    @staticmethod
#    def InsideBarShort(df, body2atr_t2, body2atr):
#        # T-2 body > 0.7 T-2 ATR
#        logic1 = CandleUtility.GetArrayT(df.BodyToATR.tolist(), -2) > body2atr_t2
#        # T body > 0.7 T ATR
#        logic2 = np.array(df.BodyToATR) > body2atr
#        # T close < T-2 low
#        logic3 = np.array(df.Close) < CandleUtility.GetArrayT(df.Low.tolist(), -2)
#        
#        # T-1 low >= T-2 low
#        logic4 = CandleUtility.GetArrayT(df.Low.tolist(), -1) \
#                >= CandleUtility.GetArrayT(df.Low.tolist(), -2)
#        # T-1 high <= T-2 high
#        logic5 = CandleUtility.GetArrayT(df.High.tolist(), -1) \
#                <= CandleUtility.GetArrayT(df.High.tolist(), -2)
#                
#        # T-1 close < T-2 close
#        logic6 = CandleUtility.GetArrayT(df.Close.tolist(), -1) \
#                < CandleUtility.GetArrayT(df.Close.tolist(), -2) 
#        
#        return logic1 & logic2 & logic3 & ((logic4 & logic5) | (logic4 & logic6))
#        
#        
    @staticmethod
    def InsideBarLong(df, bar2atr_t2, bar2atr):
        # T-2 bar > 0.7 T-2 ATR
        logic1 = CandleUtility.GetArrayT(df.BarToATR.tolist(), -2) > bar2atr_t2
        # T bar > 0.7 T ATR
        logic2 = np.array(df.BarToATR) > bar2atr
        # T close > T-2 high
        logic3 = np.array(df.Close) > CandleUtility.GetArrayT(df.High.tolist(), -2)
        
        # T-1 low >= T-2 low
        logic4 = CandleUtility.GetArrayT(df.Low.tolist(), -1) \
                >= CandleUtility.GetArrayT(df.Low.tolist(), -2)
        # T-1 high <= T-2 high
        logic5 = CandleUtility.GetArrayT(df.High.tolist(), -1) \
                <= CandleUtility.GetArrayT(df.High.tolist(), -2)
                
        # T-1 close > T-2 close
        logic6 = CandleUtility.GetArrayT(df.Close.tolist(), -1) \
                > CandleUtility.GetArrayT(df.Close.tolist(), -2) 
        
        return logic1 & logic2 & logic3 & ((logic4 & logic5) | (logic5 & logic6))
        
    @staticmethod
    def InsideBarShort(df, bar2atr_t2, bar2atr):
        # T-2 bar > 0.7 T-2 ATR
        logic1 = CandleUtility.GetArrayT(df.BarToATR.tolist(), -2) > bar2atr_t2
        # T bar > 0.7 T ATR
        logic2 = np.array(df.BarToATR) > bar2atr
        # T close < T-2 low
        logic3 = np.array(df.Close) < CandleUtility.GetArrayT(df.Low.tolist(), -2)
        
        # T-1 low >= T-2 low
        logic4 = CandleUtility.GetArrayT(df.Low.tolist(), -1) \
                >= CandleUtility.GetArrayT(df.Low.tolist(), -2)
        # T-1 high <= T-2 high
        logic5 = CandleUtility.GetArrayT(df.High.tolist(), -1) \
                <= CandleUtility.GetArrayT(df.High.tolist(), -2)
                
        # T-1 close < T-2 close
        logic6 = CandleUtility.GetArrayT(df.Close.tolist(), -1) \
                < CandleUtility.GetArrayT(df.Close.tolist(), -2) 
        
        return logic1 & logic2 & logic3 & ((logic4 & logic5) | (logic4 & logic6))
                    
                    
    # Inside Bar 1
    # Rules (Long)
    # 1.       T-2 Bar > 0.8*ATR
    # 2.       T-2 = Filled Bar
    # 3.       T Close > T-2 Open
    # 4.       T High > T-2 High
    # 5.       T-1 Low >= T-2 Low
    # 6.       T-1 High <= T-2 High
    # 7.       T-1 Close >= T-2 Close
    @staticmethod
    def InsideBar1Long(df, bart22atr):
        if(set(['Bar', 'ATR', 'Low', 'High', 'Open', 'Close']).issubset(df.columns)):
            logic1 = CandleUtility.GetArrayT(df.Bar.tolist(), -2) \
                > bart22atr * np.array(df.ATR)
            logic2 = CandleUtility.GetArrayT(df.Close.tolist(), -2) \
                < CandleUtility.GetArrayT(df.Open.tolist(), -2) # T-2 filled bar
            logic3 = np.array(df.Close) > CandleUtility.GetArrayT(df.Open.tolist(), -2)
            logic4 = np.array(df.High) > CandleUtility.GetArrayT(df.High.tolist(), -2)
            logic5 = CandleUtility.GetArrayT(df.Low.tolist(), -1) \
                >= CandleUtility.GetArrayT(df.Low.tolist(), -2)
            logic6 = CandleUtility.GetArrayT(df.High.tolist(), -1) \
                <= CandleUtility.GetArrayT(df.High.tolist(), -2)
            logic7 = CandleUtility.GetArrayT(df.Close.tolist(), -1) \
                >= CandleUtility.GetArrayT(df.Close.tolist(), -2)

            return logic1 & logic2 & logic3 & logic4 & logic5 & logic6 & logic7
        else:
            raise Exception('CandleShape: Invalid dataframe!')

    # Inside Bar 1
    # Rules (Short)
    # 1.       T-2 Bar > 0.8*ATR
    # 2.       T-2 = White Bar
    # 3.       T Close < T-2 Open
    # 4.       T Low < T-2 Low
    # 5.       T-1 Low >= T-2 Low
    # 6.       T-1 High <= T-2 High
    # 7.       T-1 Close >= T-2 Close
    @staticmethod
    def InsideBar1Short(df, bart22atr):
        if(set(['Bar', 'ATR', 'Low', 'High', 'Open', 'Close']).issubset(df.columns)):
            logic1 = CandleUtility.GetArrayT(df.Bar.tolist(), -2) \
                > bart22atr * np.array(df.ATR)
            logic2 = CandleUtility.GetArrayT(df.Close.tolist(), -2) \
                > CandleUtility.GetArrayT(df.Open.tolist(), -2) # T-2 white bar
            logic3 = np.array(df.Close) < CandleUtility.GetArrayT(df.Open.tolist(), -2)
            logic4 = np.array(df.Low) > CandleUtility.GetArrayT(df.Low.tolist(), -2)
            logic5 = CandleUtility.GetArrayT(df.Low.tolist(), -1) \
                >= CandleUtility.GetArrayT(df.Low.tolist(), -2)
            logic6 = CandleUtility.GetArrayT(df.High.tolist(), -1) \
                <= CandleUtility.GetArrayT(df.High.tolist(), -2)
            logic7 = CandleUtility.GetArrayT(df.Close.tolist(), -1) \
                >= CandleUtility.GetArrayT(df.Close.tolist(), -2)

            return logic1 & logic2 & logic3 & logic4 & logic5 & logic6 & logic7
        else:
            raise Exception('CandleShape: Invalid dataframe!')

    # Inside bar 2
    # Rules (Long)
    # 1.       T-2  Bar > 0.8*ATR
    # 2.       T-2 = Filled Bar
    # 3.       T Close > T-2 Open
    # 4.       T High > T-2 High
    # 5.       T-1 High <= T-2 High
    # 6.       T-1 Close >= T-2 Close
    # 7.       T-1 Bar < 0.8*ATR
    # 8.       T-1 Body < 0.7*Bar
    @staticmethod
    def InsideBar2Long(df, bart22atr, bart12atr, bodyt12atr):
        if(set(['Bar', 'ATR', 'Body', 'Low', 'High', 'Open', 'Close']).issubset(df.columns)):
            logic1 = CandleUtility.GetArrayT(df.Bar.tolist(), -2) \
                > bart22atr * np.array(df.ATR)
            logic2 = CandleUtility.GetArrayT(df.Close.tolist(), -2) \
                < CandleUtility.GetArrayT(df.Open.tolist(), -2) # T-2 filled bar
            logic3 = np.array(df.Close) > CandleUtility.GetArrayT(df.Open.tolist(), -2)
            logic4 = np.array(df.High) > CandleUtility.GetArrayT(df.High.tolist(), -2)
            logic5 = CandleUtility.GetArrayT(df.High.tolist(), -1) \
                <= CandleUtility.GetArrayT(df.High.tolist(), -2)
            logic6 = CandleUtility.GetArrayT(df.Close.tolist(), -1) \
                >= CandleUtility.GetArrayT(df.Close.tolist(), -2)
            logic7 = CandleUtility.GetArrayT(df.Bar.tolist(), -1) \
                < bart12atr * np.array(df.ATR)
            logic8 = CandleUtility.GetArrayT(df.Body.tolist(), -1) \
                < bodyt12atr * np.array(df.Bar)

            return logic1 & logic2 & logic3 & logic4 & logic5 & logic6 & logic7 & logic8
        else:
            raise Exception('CandleShape: Invalid dataframe!')

    # Inside Bar 2
    # Rules (Short)
    # 1.       T-2  Bar > 0.8*ATR
    # 2.       T-2 = White Bar
    # 3.       T Close < T-2 Open
    # 4.       T Low < T-2 Low
    # 5.       T-1 High <= T-2 High
    # 6.       T-1 Close >= T-2 Close
    # 7.       T-1 Bar < 0.8*ATR
    # 8.       T-1 Body < 0.7*Bar
    @staticmethod
    def InsideBar2Short(df, bart22atr, bart12atr, bodyt12atr):
        if(set(['Bar', 'ATR', 'Body', 'Low', 'High', 'Open', 'Close']).issubset(df.columns)):
            logic1 = CandleUtility.GetArrayT(df.Bar.tolist(), -2) \
                > bart22atr * np.array(df.ATR)
            logic2 = CandleUtility.GetArrayT(df.Close.tolist(), -2) \
                > CandleUtility.GetArrayT(df.Open.tolist(), -2) # T-2 white bar
            logic3 = np.array(df.Close) < CandleUtility.GetArrayT(df.Open.tolist(), -2)
            logic4 = np.array(df.Low) < CandleUtility.GetArrayT(df.Low.tolist(), -2)
            logic5 = CandleUtility.GetArrayT(df.High.tolist(), -1) \
                <= CandleUtility.GetArrayT(df.High.tolist(), -2)
            logic6 = CandleUtility.GetArrayT(df.Close.tolist(), -1) \
                >= CandleUtility.GetArrayT(df.Close.tolist(), -2)
            logic7 = CandleUtility.GetArrayT(df.Bar.tolist(), -1) \
                < bart12atr * np.array(df.ATR)
            logic8 = CandleUtility.GetArrayT(df.Body.tolist(), -1) \
                < bodyt12atr * np.array(df.Bar)

            return logic1 & logic2 & logic3 & logic4 & logic5 & logic6 & logic7 & logic8
        else:
            raise Exception('CandleShape: Invalid dataframe!')
            
    # PureInsideBar
    # Rules
    # 1.       T High <= T-1 High
    # 2.       T max(Open, Close) <= T-1 max(Open, Close)
    # 3.       T Low >= T-1 Low
    # 4.       T min(Open, Close) >= T-1 min(Open, Close)
    @staticmethod
    def PureInsideBar(df):
        if(set(['Low', 'High', 'Open', 'Close']).issubset(df.columns)):
            logic1 = np.array(df.High) <= CandleUtility.GetArrayT(df.High.tolist(), -1)
#            logic2 = np.max([np.array(df.Open), np.array(df.Close)]) \
#                    <= np.max([CandleUtility.GetArrayT(df.Open.tolist(), -1), CandleUtility.GetArrayT(df.Close.tolist(), -1)])
            logic3 = np.array(df.Low) >= CandleUtility.GetArrayT(df.Low.tolist(), -1)
#            logic4 = np.min([np.array(df.Open), np.array(df.Close)]) \
#                    >= np.min([CandleUtility.GetArrayT(df.Open.tolist(), -1), CandleUtility.GetArrayT(df.Close.tolist(), -1)])
             
            logic2 = True
            logic4 = True
            return logic1 & logic2 & logic3 & logic4
        else:
            raise Exception('CandleShape: Invalid dataframe!')
            
    # Breakout
    # Rules (Long)
    # 1.       T Bar > 0.8*ATR
    # 1.       T High > T-1 High
    # 2.       T Close > T-1 Close
    @staticmethod
    def BreakoutLong(df, bar2atr):
        if(set(['InsideBarPure', 'Open', 'Close', 'Bar', 'ATR']).issubset(df.columns)):
            signal = [0]
            logic1 = np.array(df.Bar) > bar2atr * np.array(df.ATR)
            logic2 = np.array(df.High) > CandleUtility.GetArrayT(df.High.tolist(), -1)
            logic3 = np.array(df.Close) > CandleUtility.GetArrayT(df.Close.tolist(), -1)
            for i in xrange(1, len(logic1)):
                logic = logic1[i] & logic2[i] & logic3[i]
                if logic:
                    # date i is a breakout
                    j = 0
                    while(df.InsideBarPure[i-j-1]):
                        j += 1
                        
                    signal.append(j)
                else:
                    signal.append(0)
                    
            return np.array(signal)
        else:
            raise Exception('CandleShape: Invalid dataframe!')
            
            
    # Breakout
    # Rules (Short)
    # 1.       T Bar > 0.8*ATR
    # 1.       T Low < T-1 Low
    # 2.       T Close < T-1 Close
    @staticmethod
    def BreakoutShort(df, bar2atr):
        if(set(['InsideBarPure', 'Open', 'Close', 'Bar', 'ATR']).issubset(df.columns)):
            signal = [0]
            logic1 = np.array(df.Bar) > bar2atr * np.array(df.ATR)
            logic2 = np.array(df.Low) < CandleUtility.GetArrayT(df.Low.tolist(), -1)
            logic3 = np.array(df.Close) < CandleUtility.GetArrayT(df.Close.tolist(), -1)
            for i in xrange(1, len(logic1)):
                logic = logic1[i] & logic2[i] & logic3[i]
                if logic:
                    # date i is a breakout
                    j = 0
                    while(df.InsideBarPure[i-j-1]):
                        j += 1
                        
                    signal.append(-j)
                else:
                    signal.append(0)
                    
            return np.array(signal)
        else:
            raise Exception('CandleShape: Invalid dataframe!')
        