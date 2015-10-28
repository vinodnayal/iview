import pandas as pd
from dao import dbdao
from bl import rsi_manager
from util import  constants, alert_constants



def smacrossovers(df_merged):
    give_positive_co_dates(df_merged,'close','sma50',alert_constants.Crossed_above_SMA_50, 'Stock Breaks above 50 days SMA')
    give_positive_co_dates(df_merged,'close','sma100',alert_constants.Crossed_above_SMA_100,'Stock Breaks above 100 days SMA')
    give_positive_co_dates(df_merged,'close','sma150',alert_constants.Crossed_above_SMA_150,'Stock Breaks above 150 days SMA')
    give_positive_co_dates(df_merged,'close','sma200',alert_constants.Crossed_above_SMA_200,'Stock Breaks above 200 days SMA')
    
    give_positive_co_dates(df_merged,'sma50','sma200',alert_constants.Crossed_above_SMA_50_200,'50 days SMA breaks above 200 days SMA')
    give_negative_co_dates(df_merged,'sma50','sma200',alert_constants.Crossed_below_SMA_50_200,'50 days SMA breaks below 200 days SMA')
    
    give_negative_co_dates(df_merged,'close','sma50',alert_constants.Crossed_below_SMA_50,'Stock Breaks below 50 days SMA')
    give_negative_co_dates(df_merged,'close','sma100',alert_constants.Crossed_below_SMA_100,'Stock Breaks below 100 days SMA')
    give_negative_co_dates(df_merged,'close','sma150',alert_constants.Crossed_below_SMA_150,'Stock Breaks below 150 days SMA')
    give_negative_co_dates(df_merged,'close','sma200',alert_constants.Crossed_below_SMA_200,'Stock Breaks below 200 days SMA')
    
def give_positive_co_dates(df,column1,column2,typeid,text):

    previous_col1 = df[column1].shift(1)
    previous_col2 = df[column2].shift(1)
    crossing = ((df[column1] >= df[column2]) & (previous_col1 <= previous_col2))
    crossing_dates = df.loc[crossing]
    crossing_dates['sign']=1
    crossing_dates['typeid']=typeid
    crossing_dates['text']=text
   
    dbdao.savealerts(crossing_dates)
    
def give_negative_co_dates(df,column1,column2,typeid,text):

    previous_col1 = df[column1].shift(1)
    previous_col2 = df[column2].shift(1)
    crossing = ((df[column1] <= df[column2]) & (previous_col1 >= previous_col2))            
    crossing_dates = df.loc[crossing]
    crossing_dates['sign']=-1
    crossing_dates['typeid']=typeid
    crossing_dates['text']=text
    
    dbdao.savealerts(crossing_dates)
    

def bullish_above(df,column1):
    crossing = ((df[column1] >=0) )
    crossing_dates = df.loc[crossing]
    print crossing_dates

def bearish_below(df,column1):
    crossing = ((df[column1] >=0) )                
    crossing_dates = df.loc[crossing]
    print crossing_dates
    

def obos_alerts(df):
    df['rsi_value'] = df['rsi'].apply(rsi_manager.calculate_rsi_values )
    df_aos = df.loc[df['rsi_value'] ==constants.RSI_ApproachingOversold]
    df_aos['sign']=1
    df_aos['typeid']=alert_constants.ApproachingOversold
    df_aos['text']='ApproachingOversold'
    
    
    df_os = df.loc[(df['rsi_value'] ==constants.RSI_Oversold)]
    df_os['sign']=1
    df_os['typeid']=alert_constants.Oversold
    df_os['text']='Oversold'
    
    
    df_aob= df.loc[(df['rsi_value'] ==constants.RSI_ApproachingOverbought)]
    df_aob['sign']=-1
    df_aob['typeid']=alert_constants.ApproachingOverbought
    df_aob['text']='ApproachingOverbought'
    
    
    df_ob = df.loc[(df['rsi_value'] ==constants.RSI_Overbought)]
    df_ob['sign']=-1
    df_ob['typeid']=alert_constants.Overbought
    df_ob['text']='Overbought'
    
    
    df_merged = pd.concat([df_aob,df_aos,df_os,df_ob],axis=0)
   
     
    dbdao.savealerts(df_merged)
    
def macd_crossovers(df):  
    df_bull_signal= bullish_co(df, 'macdhist',alert_constants.MACD_ABOVE_SIGNAL,'MACD crosses above signal line')    
    df_bear_signal=bearish_co(df, 'macdhist',alert_constants.MACD_BELOW_SIGNAL,'MACD crosses below signal line')
    df_bull_center= bullish_co(df, 'macd',alert_constants.MACD_ABOVE_CENTER,'MACD crosses above center line')
    df_bear_center=bearish_co(df, 'macd',alert_constants.MACD_BELOW_CENTER,'MACD crosses below center line')
    df_merged=pd.concat([df_bull_signal,df_bear_signal,df_bull_center,df_bear_center],axis=0)  
  
    dbdao.savealerts(df_merged) 
        
def bullish_co(df,column1,typeid,text):
    previous = df[column1].shift(1)   
    crossing = ((df[column1] >=0) & (previous <0))
    crossing_dates = df.loc[crossing]
    crossing_dates['sign']=1
    crossing_dates['text']=text
    crossing_dates['typeid']=typeid
    return crossing_dates
    
def TrendChangePositive(df,column1,typeid):
 
    crossing = ((df[column1] >df[column1].shift(1) ))
    crossing_dates = df.loc[crossing]
    crossing_dates['sign']=1
    crossing_dates['typeid']=typeid
    
    df_alerts=crossing_dates.rename(columns={column1: "newvalue"})
    dbdao.savealerts(df_alerts)
def TrendChangeNegative(df,column1,typeid):
 
    crossing = ((df[column1] <df[column1].shift(1) ))
    crossing_dates = df.loc[crossing]
    crossing_dates['sign']=-1
    crossing_dates['typeid']=typeid
    df_alerts=crossing_dates.rename(columns={column1: "newvalue"})
    dbdao.savealerts(df_alerts)

def bearish_co(df,column1,typeid,text):
    previous = df[column1].shift(1)
    crossing =  ((df[column1]<= 0) & (previous >0))
    crossing_dates = df.loc[crossing]
    crossing_dates['sign']=-1
    crossing_dates['text']=text
    crossing_dates['typeid']=typeid
    return crossing_dates
    
    