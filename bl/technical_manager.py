
from util import  constants
import talib
from talib import MA_Type
import numpy as np
from talib import abstract
import math
import matplotlib.pyplot as plt

import pandas as pd
from bl import price_manager


def calculate_stddev(df):

    returns = df.pct_change()
    stddev= returns.std()
    stddev= stddev.iloc[0]
    
    volatility= stddev* 100 * math.sqrt(252)
    
    return {"stddev":stddev,"volatility":volatility}

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
    for hist_date_tuple in hist_dates:            
            hist_date=hist_date_tuple[1]
            price=price_manager.get_price_date(df,hist_date)
            dates_prices.update({"price_"+hist_date_tuple[0]:price})
    
    return dates_prices

def calculate_res_sup(df):
    latest_row = df.tail(1).iloc[0]
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
    return {"r1":r1,"s1":s1,"r2":r2,"s2":s2,"r3":r3,"s3":s3}



def calculate_technical(df_symbol,symbol,df_mkt,start_date_time,end_date_time,hist_dates): 
    
    list_drop_cloumns = [ 'open', 'high','low']
    df_symbol_close = df_symbol.drop(list_drop_cloumns,1)
    df_mkt_close = df_mkt.drop(list_drop_cloumns,1)
    
    
    
    return_data={}
    return_data.update(calculate_stddev(df_symbol_close))
    return_data.update(calculate_beta(df_symbol_close,df_mkt_close,symbol))
    return_data.update( calculate_res_sup(df_symbol))
    return_data.update(  calculate_prices_at_dates(df_mkt_close,hist_dates))
    print return_data
    
    mom=abstract.MOM(df_symbol_close, timeperiod=5)

    rsi=abstract.RSI(df_symbol_close).round(2)    
    sma20 = abstract.SMA(df_symbol_close, timeperiod=20).round(2)
    sma50 = abstract.SMA(df_symbol_close, timeperiod=50).round(2)
    sma100 = abstract.SMA(df_symbol_close, timeperiod=100).round(2)
    sma200 = abstract.SMA(df_symbol_close, timeperiod=200).round(2)
    
    macd=abstract.MACD(df_symbol_close)
    df_merged=macd.apply(np.round)
    
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
    df_latest=df_merged.tail(1)
    
    for key, value in return_data.iteritems():
        
        df_latest[key]=value
    
    return df_latest
    
    
    


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
    