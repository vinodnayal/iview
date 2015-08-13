
from util import  constants
import talib
from talib import MA_Type
import numpy as np
from talib import abstract
import math
import matplotlib.pyplot as plt
from dao import dbdao
import pandas as pd
from bl import price_manager, rating_manager
from bl import Long_Short





def calculate_stdabove(latest_row):   
    price=latest_row['close']
    sma50=latest_row['sma50']
    volatility=latest_row['volatility']
    std_above=0
    if(volatility!=0):    
        std_above= (100*(price-sma50)/price)/ volatility
    return std_above


def calculate_beta(df,df_mkt,symbol):
    
    if(symbol==constants.MKT_SYMBOL):
        return {"beta":1}
    
    df = df.rename(columns={constants.CLOSE: constants.MKT_SYMBOL})
    df_mkt = df_mkt.rename(columns={constants.CLOSE: symbol})[symbol]
    df_merged = df.join(df_mkt)
    
   
    returns = df_merged.pct_change()
    variance = returns.var() 
    covariance = returns.cov()
    beta = covariance.loc[symbol, constants.MKT_SYMBOL] / variance.loc[constants.MKT_SYMBOL]
    return {"beta":beta}

def calculate_prices_at_dates(df,hist_dates):
    
    dates_prices={}
    for type,date in hist_dates.iteritems():            
           
            price=price_manager.get_price_date(df,date)
            dates_prices.update({"price_"+type:price})
    
    return dates_prices

def calc_res(latest_row):
    H = latest_row[constants.HIGH]
    L = latest_row[constants.LOW]
    C = latest_row[constants.CLOSE]
    P = (H + L + C) / 3.0;
    r1 = 2 * P - L;
    s1 = 2 * P - H;
    r2 = P + (H - L);
    s2 = P - (H - L);
    r3 = H + 2 * (P - L);
    s3 = L - 2 * (H - P);  
    return pd.Series({'r1': r1, 'r2': r2,'r3':r3,'s1': s1, 's2': s2,'s3':s3})
    
    
    


    


def calculate_technical(df_symbol,symbol,df_mkt,start_date_time,end_date_time,hist_dates,days_back): 
    
    
    
    
    
    
    
    
    
    list_drop_cloumns = [ 'open', 'high','low']
    df_symbol_close = df_symbol.drop(list_drop_cloumns,1)
    df_mkt_close = df_mkt.drop(list_drop_cloumns,1)
    
    
    
    
    
    mom=abstract.MOM(df_symbol_close, timeperiod=5)
    
    macd=abstract.MACD(df_symbol_close)
    df_merged=macd.apply(np.round)
    df_std= abstract.STDDEV(df_symbol_close.pct_change(),timeperiod=100)
    df_merged['stddev']=df_std
    df_merged['volatility']=df_std*100*math.sqrt(252)
    
    
    rsi=abstract.RSI(df_symbol_close).round(2)    
    sma20 = abstract.SMA(df_symbol_close, timeperiod=20).round(2)
    
    sma50 = abstract.SMA(df_symbol_close, timeperiod=50).round(2)
    sma100 = abstract.SMA(df_symbol_close, timeperiod=100).round(2)
    sma200 = abstract.SMA(df_symbol_close, timeperiod=200).round(2)
    sma3 = abstract.SMA(df_symbol_close, timeperiod=3).round(2)
    
    sma5 = abstract.SMA(df_symbol_close, timeperiod=5).round(2)
    #print sma20,sma50
    sma9 = abstract.SMA(df_symbol_close, timeperiod=9).round(2)
    
    sma13 = abstract.SMA(df_symbol_close, timeperiod=13).round(2)
    
        
    
    sma25 = abstract.SMA(df_symbol_close, timeperiod=25).round(2)
    
    sma50 = abstract.SMA(df_symbol_close, timeperiod=50).round(2)
    
    sma90 = abstract.SMA(df_symbol_close, timeperiod=90).round(2)
    
    sma36 = abstract.SMA(df_symbol_close, timeperiod=36).round(2)
    
    sma150 = abstract.SMA(df_symbol_close, timeperiod=150).round(2)
   
    
    
    
    df_merged['mom']=mom
    df_merged['sma20']=sma20
    df_merged['sma50']=sma50
    df_merged['sma100']=sma100
    df_merged['sma200']=sma200
    df_merged['rsi']=rsi    
    df_merged['close']=df_symbol_close
    
    df_merged=df_merged.dropna()
    df_merged['symbol']=symbol
    df_merged['rsi_value'] = df_merged['rsi'].apply(calculate_rsi_values )
    df_merged['sma3']=sma3
    df_merged['sma5']=sma5
    df_merged['sma9']=sma9
    df_merged['sma13']=sma13
    df_merged['sma20']=sma20
    df_merged['sma25']=sma25
    df_merged['sma50']=sma50
    df_merged['sma90']=sma90
    df_merged['sma36']=sma36
    df_merged['sma150']=sma150
    
    df_merged['stdabove']=df_merged.apply(calculate_stdabove,axis=1)
    
    
    df_merged[['r1','r2','r3','s1','s2','s3']]=df_symbol.apply(calc_res,axis=1)
    
    
    
    
    
    df_rating=rating_manager.calc_rating(df_merged, days_back, symbol)
    
    df_merged['rating']=df_rating['rating']
    df_merged=df_merged.dropna()
    
    
    
    #latest data calculations
    return_data={}
    
    return_data.update(calculate_beta(df_symbol_close,df_mkt_close,symbol))
    
    return_data.update(  calculate_prices_at_dates(df_symbol_close,hist_dates))
    
    monthly_date = hist_dates['Monthly']
    weekly_date = hist_dates['Weekly']
    
    print price_manager.get_specific_date_value(df_merged,monthly_date,'volatility')
    print price_manager.get_specific_date_value(df_merged,weekly_date,'volatility')
    exit()
    df_latest=df_merged.tail(1)    
    latest_row=df_merged.tail(1).iloc[0]
    return_data.update(trend_calculation(latest_row))    
    
    
    for key, value in return_data.iteritems():
        
        df_latest[key]=value
    
    
    
    return df_latest
    
    
    
def trend_calculation(latest_row):
     
   
   
    r1=Long_Short.Short_term(latest_row)
    short_term_trend=0
    if r1 >= 5:
        short_term_trend=constants.VERY_BULLISH
             
    if r1 >= 3 and r1 <5:
        short_term_trend=constants.BULLISH
        
    if r1 >= 2 and r1 <3:
        short_term_trend=constants.NEUTRAL
    if r1 >= 1 and r1 <2:
        short_term_trend=constants.BEARISH
        
    if r1 == 0 :
        short_term_trend=constants.VERY_BEARISH
                      
    r2=Long_Short.Intermediate_term(latest_row)
    Inter_term_trend=0
    if r2 >= 2:
        Inter_term_trend=constants.VERY_BULLISH
        
    if r2 >= 1 and r2 <2:
        Inter_term_trend=constants.BULLISH
        
    if r2 == 0:
        Inter_term_trend=constants.NEUTRAL
        
    r3=Long_Short.Long_term(latest_row)
    long_term_trend=0
    if r3 >= 2:
        long_term_trend=constants.VERY_BULLISH
        
    if r3 >= 1 and r3 <2:
        long_term_trend=constants.BULLISH
        
    if r3 == 0:
        long_term_trend=constants.NEUTRAL
    
    
    rsi_current=latest_row['rsi']
    rsi_current_text=calculate_rsi_values(rsi_current)
    
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
    
    if( inter_term_sign==1 and long_term_sign==1 and rsi_current_text==constants.RSI_Neutral):
        synopsis_rule_id=1
    
    elif(inter_term_sign==1 and long_term_sign==1 and rsi_current_text==constants.RSI_ApproachingOverbought):
        synopsis_rule_id=6
        
    elif(inter_term_sign==1 and long_term_sign==1 and rsi_current_text==constants.RSI_Overbought):
        synopsis_rule_id=7    
        
    elif(inter_term_sign==1 and long_term_sign==1 and rsi_current_text==constants.RSI_ExtremelyOverbought):
        synopsis_rule_id=8
        
    elif(short_term_sign==-1 and inter_term_sign==1 and long_term_sign==1):
        synopsis_rule_id=2         
             
    elif(short_term_sign==-1 and inter_term_sign==1 and long_term_sign==-1):
        synopsis_rule_id=3
        
    elif(short_term_sign==1 and inter_term_sign==1 and long_term_sign==-1):
        synopsis_rule_id=9             
        
    elif(short_term_sign==-1 and inter_term_sign==-1 and long_term_sign==1):
        synopsis_rule_id=10    
        
    elif(short_term_sign==-1 and inter_term_sign==-1 and long_term_sign==-1):
        synopsis_rule_id=4
        
    elif(short_term_sign==1 and inter_term_sign==-1 and long_term_sign==-1):
        synopsis_rule_id=5    
    
    #print short_term_trend,Inter_term_trend,long_term_trend,synopsis_rule_id
    return {"short_trend":short_term_trend,"inter_trend":Inter_term_trend,"long_trend":long_term_trend,"synopsis_rule_id":synopsis_rule_id}




def calculate_sma_co(x):
    x1=x['sma200_price_diff']
    x2=x['sma200_price_diff_shifted']
    if(x1>=0 and x2 >=0):
        return 0
    elif(x1<=0 and x2 <=0):
        return 0
    elif(x1>=0 and x2<0):
        return 1
    else:
        return -1

def calculate_rsi_values(p):
    
            if (p < 20 ):
            
                r = constants.RSI_ExtremelyOversold
            
            elif (p >= 20 and p <= 30):
            
                r = constants.RSI_Oversold
            
            elif (p > 30 and p <= 45):
            
                r = constants.RSI_ApproachingOversold
            
            elif (p > 45 and p <= 55):
            
                r = constants.RSI_Neutral
            
            elif (p > 55 and p <= 70):
            
                r = constants.RSI_ApproachingOverbought           
           
            elif (p > 70 and p <= 80):
            
                r = constants.RSI_Overbought
            
            elif (p > 80):
            
                r = constants.RSI_ExtremelyOverbought
                
            return r



    