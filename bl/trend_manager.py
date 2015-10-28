from util import  constants
import talib
from talib import MA_Type
import numpy as np
from talib import abstract
import math
import matplotlib.pyplot as plt
from dao import dbdao
import pandas as pd
from bl import price_manager, rating_manager, rsi_manager

def trend_calculation(latest_row):
     
   
   
    short_term_trend=Short_term(latest_row)
    
                      
    Inter_term_trend=Intermediate_term(latest_row)
    
        
    long_term_trend=Long_term(latest_row)
    
    
    
    
    rsi_current_value=latest_row['rsi_value']
    
    short_term_sign=-1
    inter_term_sign=-1
    long_term_sign=-1
    
    if(short_term_trend==constants.BULLISH or short_term_trend==constants.VERY_BULLISH):
        short_term_sign=1  
    
    if(Inter_term_trend==constants.BULLISH or Inter_term_trend==constants.VERY_BULLISH):
        inter_term_sign=1
    
    if(long_term_trend==constants.BULLISH or long_term_trend==constants.VERY_BULLISH):
        long_term_sign=1
    
    
    synopsis_rule_id=-1
    
    
    
    
    if( short_term_sign ==1   ):
        
        if(inter_term_sign==1 and long_term_sign==1):
            synopsis_rule_id=11 # default for all positive
        
            if( rsi_current_value==constants.RSI_Neutral ):
                synopsis_rule_id=1
             
            elif( rsi_current_value==constants.RSI_ApproachingOverbought):
                synopsis_rule_id=6
                
            elif( rsi_current_value==constants.RSI_Overbought):
                synopsis_rule_id=7    
                
            elif( rsi_current_value==constants.RSI_ExtremelyOverbought):
                synopsis_rule_id=8
        
        elif(inter_term_sign==1 and long_term_sign==-1):
            synopsis_rule_id=9
        elif(inter_term_sign==-1 and long_term_sign==-1):
            synopsis_rule_id=5
        elif(inter_term_sign==-1 and long_term_sign==1):
            synopsis_rule_id=12 
        
        
        
    elif(short_term_sign==-1):
        if(inter_term_sign==1 and long_term_sign==1):
            synopsis_rule_id=2         
             
        elif(inter_term_sign==1 and long_term_sign==-1):
            synopsis_rule_id=3
        
                 
        
        elif(inter_term_sign==-1 and long_term_sign==1):
            synopsis_rule_id=10    
        
        elif( inter_term_sign==-1 and long_term_sign==-1):
            synopsis_rule_id=4
        
       
    
    #print short_term_trend,Inter_term_trend,long_term_trend,synopsis_rule_id
    return pd.Series({"short_trend":short_term_trend,"inter_trend":Inter_term_trend,"long_trend":long_term_trend,"synopsis_rule_id":synopsis_rule_id})




def macd_term(latest_row):

    short_sum=0
    
         
    if(latest_row['macdhist']>=0) :
        short_sum=short_sum+1
    else:
        short_sum=short_sum -1
    if(latest_row['macd']>=0) :
        short_sum=short_sum+1 
    else:
        short_sum=short_sum - 1
        
        
    if(short_sum==-2):
         return constants.VERY_BEARISH
   
    elif(short_sum==2):  
         return constants.VERY_BULLISH 
    else :
        return constants.NEUTRAL
        

def Short_term(latest_row):

    short_sum=0
    
    if (latest_row['sma3'] >= latest_row['sma9']):
        short_sum=short_sum+1
    else:
        short_sum=short_sum -1 
         
    if (latest_row['sma5']) >= (latest_row['sma13']):
        short_sum=short_sum+1
    else:   
        short_sum=short_sum -1
        
    if (latest_row['sma5']) >= (latest_row['sma20']):
        short_sum=short_sum+1
    else:
        short_sum=short_sum-1
    
    if (latest_row['rsi']) >= 50:
        short_sum=short_sum+1
   
    if (latest_row['rsi']) < 30:
        short_sum=short_sum-1
        
    if(latest_row['macdhist']>=0) :
        short_sum=short_sum+1
    else:
        short_sum=short_sum -1
    if(latest_row['macd']>=0) :
        short_sum=short_sum+1 
    else:
        short_sum=short_sum - 1
        
   
    
    r1= short_sum  
    short_term_trend=constants.NEUTRAL
    if r1 >= 5:
        short_term_trend=constants.VERY_BULLISH
             
    if r1 >= 3 and r1 <5:
        short_term_trend=constants.BULLISH
        
    if r1 >= 2 and r1 <3:
        short_term_trend=constants.NEUTRAL
    if r1 >= 1 and r1 <2:
        short_term_trend=constants.BEARISH
        
    else:
        short_term_trend=constants.VERY_BEARISH 
     
    return short_term_trend   
    

def Intermediate_term(latest_row):

    inter_sum=0
    
    if (latest_row['sma25'] >= latest_row['sma90']):
        inter_sum=inter_sum+1
    else:   
        inter_sum=inter_sum -1
          
    if (latest_row['sma13']) >= (latest_row['sma50']):
        inter_sum=inter_sum+1
    else:    
        inter_sum=inter_sum-1

   
    
    r2= inter_sum 
    Inter_term_trend=constants.NEUTRAL  
    if r2 >= 2:
        Inter_term_trend=constants.VERY_BULLISH
        
    elif r2 >= 1:
        Inter_term_trend=constants.BULLISH
        
    else:
        Inter_term_trend=constants.NEUTRAL  
    return     Inter_term_trend
    
   
def Long_term(latest_row):

    long_sum=0
    
    if (latest_row['sma36'] >= latest_row['sma150']):
        long_sum=long_sum+1
    else:
        long_sum=long_sum -1 
     
    if (latest_row['sma50']) >= (latest_row['sma200']):
        long_sum=long_sum+1
    else:    
        long_sum=long_sum -1 

    r3= long_sum
    long_term_trend=constants.NEUTRAL 
    if r3 >= 2:
        long_term_trend=constants.VERY_BULLISH
        
    elif r3 >= 1 :
        long_term_trend=constants.BULLISH
        
    else:
        long_term_trend=constants.NEUTRAL        
    return long_term_trend

