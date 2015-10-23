import pandas as pd
from dao import dbdao
from bl import rsi_manager
from util import  constants



    
def give_positive_co_dates(df,column1,column2,text):

    previous_col1 = df[column1].shift(1)
    previous_col2 = df[column2].shift(1)
    crossing = ((df[column1] >= df[column2]) & (previous_col1 <= previous_col2))
    crossing_dates = df.loc[crossing]
    crossing_dates['sign']=1
    crossing_dates['typeid']=9
    crossing_dates['text']=text
    df_alerts= crossing_dates[['sign','typeid','symbol','text']]
    dbdao.save_dataframe(df_alerts, "df_alerts")
    
def give_negative_co_dates(df,column1,column2,text):

    previous_col1 = df[column1].shift(1)
    previous_col2 = df[column2].shift(1)
    crossing = ((df[column1] <= df[column2]) & (previous_col1 >= previous_col2))            
    crossing_dates = df.loc[crossing]
    crossing_dates['sign']=-1
    crossing_dates['typeid']=10
    crossing_dates['text']=text
    df_alerts= crossing_dates[['sign','typeid','symbol','text']]
    dbdao.save_dataframe(df_alerts, "df_alerts")
    

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
    df_aos['typeid']=5
    df_aos['text']='ApproachingOversold'
    
    
    df_os = df.loc[(df['rsi_value'] ==constants.RSI_Oversold)]
    df_os['sign']=1
    df_os['typeid']=6
    df_os['text']='Oversold'
    
    
    df_aob= df.loc[(df['rsi_value'] ==constants.RSI_ApproachingOverbought)]
    df_aob['sign']=-1
    df_aob['typeid']=7
    df_aob['text']='ApproachingOverbought'
    
    
    df_ob = df.loc[(df['rsi_value'] ==constants.RSI_Overbought)]
    df_ob['sign']=-1
    df_ob['typeid']=8
    df_ob['text']='Overbought'
    
    
    df_merged = pd.concat([df_aob,df_aos,df_os,df_ob],axis=0)
    df_alerts= df_merged[['symbol','sign','typeid','text']]
     
    dbdao.save_dataframe(df_alerts, "df_alerts")
    
def macd_crossovers(df):  
    df_bull_signal= bullish_co(df, 'macdhist',1,'MACD crosses above signal line')    
    df_bear_signal=bearish_co(df, 'macdhist',2,'MACD crosses below signal line')
    df_bull_center= bullish_co(df, 'macd',3,'MACD crosses above center line')
    df_bear_center=bearish_co(df, 'macd',4,'MACD crosses below signal line')
    df_merged=pd.concat([df_bull_signal,df_bear_signal,df_bull_center,df_bear_center],axis=0)  
    df_alerts= df_merged[['symbol','sign','typeid','text']]
    dbdao.save_dataframe(df_alerts, "df_alerts") 
        
def bullish_co(df,column1,typeid,text):
    previous = df[column1].shift(1)   
    crossing = ((df[column1] >=0) & (previous <0))
    crossing_dates = df.loc[crossing]
    crossing_dates['sign']=1
    crossing_dates['text']=text
    crossing_dates['typeid']=typeid
    return crossing_dates
    

def bearish_co(df,column1,typeid,text):
    previous = df[column1].shift(1)
    crossing =  ((df[column1]<= 0) & (previous >0))
    crossing_dates = df.loc[crossing]
    crossing_dates['sign']=-1
    crossing_dates['text']=text
    crossing_dates['typeid']=typeid
    return crossing_dates
    
    