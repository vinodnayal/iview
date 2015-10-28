
from util import  constants, loglib, alert_constants
import talib
from talib import MA_Type
import numpy as np
from talib import abstract
import math

from dao import dbdao
import pandas as pd
from bl import price_manager, rating_manager, rsi_manager, crossover_manager,\
    alert_manager
from bl import trend_manager



logger = loglib.getlogger('technicals_manager')

def calculate_stdabove(latest_row):   
    price=latest_row['close']
    sma50=latest_row['sma50']
    volatility=latest_row['volatility']
    std_above=0
    if(volatility!=0):    
        std_above= ((price-sma50))/ volatility
    return std_above


def calculate_beta(df,df_mkt,symbol):
    
    if(symbol==constants.MKT_SYMBOL):
        return {"beta":1}
    
    df = df.rename(columns={constants.CLOSE: symbol})
    df_mkt = df_mkt.rename(columns={constants.CLOSE: constants.MKT_SYMBOL})
    df_merged = df.join(df_mkt)
     
     
    #for last year 
    df_beta=df_merged.tail(252)
    
    returns = df_beta.pct_change()
    
    
    
    variance = returns.var() 
    covariance = returns.cov()
    beta = covariance.loc[symbol, constants.MKT_SYMBOL] / variance.loc[constants.MKT_SYMBOL]
    
    return {"beta":beta}

def relative_strength(df,df_mkt,symbol):
   
    df = df[['close']]#.rename(columns={constants.CLOSE: "symbol"})
    df_mkt = df_mkt[['close']]#.rename(columns={constants.CLOSE: "mkt"})
    df['Relative_strength']=100*(df['close']-df['close'].shift(120))/(df['close'].shift(120))
    df_mkt['Relative_strength']=100*(df_mkt['close']-df_mkt['close'].shift(120))/(df_mkt['close'].shift(120))
    df_merged = df[['Relative_strength']]-df_mkt[['Relative_strength']]
    return df_merged

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
    
    
def calc_signs(latest_row):
    close = latest_row['close']
    sma20 = latest_row['sma20']
    sma50 = latest_row['sma50']
    sma200 = latest_row['sma200']
    sma_20day_sign=-1
    sma_50day_sign=-1
    sma_200day_sign=-1
    if (close>sma20 ):
         sma_20day_sign=1
    if (close>sma50 ):
         sma_50day_sign=1
    if (close> sma200):
         sma_200day_sign=1
    
    data=pd.Series({'sma_20day_sign': sma_20day_sign, 'sma_50day_sign': sma_50day_sign,'sma_200day_sign':sma_200day_sign})
    #data=pd.Series(sma_20day_sign)     
    
   
    return data


def calculate_technical(df_symbol,symbol,df_mkt,start_date_time,end_date_time,hist_dates,days_back): 
 
    #list_drop_cloumns = [ 'open', 'high','low','volume']
    df_symbol_close = df_symbol[['close']]
    
    df_mkt_close = df_mkt[['close']]
    mom=abstract.MOM(df_symbol_close, timeperiod=5)    
    df_merged=abstract.MACD(df_symbol_close,fastperiod=12,slowperiod=26,signalperiod=9)
   
    #df_merged=macd.apply(np.round)
    
    df_std= abstract.STDDEV(df_symbol_close.pct_change(),timeperiod=100)
    df_merged['stddev']=df_std
    df_merged['volatility']=df_std*100*math.sqrt(252)
    rsi=abstract.RSI(df_symbol_close).round(2)    
    sma20 = abstract.SMA(df_symbol_close, timeperiod=20).round(2)

    sma100 = abstract.SMA(df_symbol_close, timeperiod=100).round(2)
    sma200 = abstract.SMA(df_symbol_close, timeperiod=200).round(2)
    sma3 = abstract.SMA(df_symbol_close, timeperiod=3).round(2)
    
    sma5 = abstract.SMA(df_symbol_close, timeperiod=5).round(2)
    
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
    df_merged['close']=df_symbol['close']
    df_merged['open']=df_symbol['open']
    df_merged['low']=df_symbol['low']
    df_merged['high']=df_symbol['high']
    df_merged['volume']=df_symbol['volume']
    df_merged['sma_volume_6month']= pd.rolling_mean(df_merged['volume'], window=120).round(2)
    df_merged=df_merged.dropna()
    df_merged['symbol']=symbol
    df_merged['rsi_value'] = df_merged['rsi'].apply(rsi_manager.calculate_rsi_values )
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
    df_merged['Relative_strength']=relative_strength(df_symbol_close, df_mkt_close, symbol)['Relative_strength']
  
    df_merged['stdabove']=df_merged.apply(calculate_stdabove,axis=1)
    
    df_merged['date']=df_merged.index
    
    df_res=df_symbol.apply(calc_res,axis=1)
    df_merged=pd.concat([df_merged,df_res],axis=1)
    df_rating=rating_manager.calc_rating_history(df_merged, days_back, symbol)
    df_trends=df_merged.apply(lambda row : trend_manager.trend_calculation(row),axis=1)

    df_merged=pd.concat([df_merged,df_trends],axis=1)
 
    crossover_manager.TrendChangePositive(df_merged,"short_trend",alert_constants.TREND_SHORT)
    crossover_manager.TrendChangePositive(df_merged,"inter_trend",alert_constants.TREND_INTERMEDIATE)
    crossover_manager.TrendChangePositive(df_merged,"long_trend",alert_constants.TREND_LONG)
    
    
    crossover_manager.TrendChangeNegative(df_merged,"short_trend",alert_constants.TREND_SHORT)
    crossover_manager.TrendChangeNegative(df_merged,"inter_trend",alert_constants.TREND_INTERMEDIATE)
    crossover_manager.TrendChangeNegative(df_merged,"long_trend",alert_constants.TREND_LONG)

    
    df_merged['rating']=df_rating['rating']
    
    df_merged=df_merged.replace([np.inf, -np.inf], np.nan)
    
    df_merged=df_merged.dropna()
    print "********************************************************************************"
    print "********************************************************************************"
    print "********************************************************************************"
    #print df_merged
   
    if(df_merged is None or df_merged.symbol.count()==0):
        return
    
    logger.info("Saving history for Symbol "+symbol + " length = "+ str(len(df_merged)))
    df_merged.set_index('date',inplace=True)  
    
    
    
    alert_manager.relative_strength(df_merged)
    
    
    alert_manager.fullGapPositive(df_merged)
    alert_manager.fullGapNegative(df_merged)
    alert_manager.partialGapPositive(df_merged)
    alert_manager.partialGapNegative(df_merged)
        
    alert_manager.keyReversalPositive(df_merged)
    alert_manager.keyReversalNegative(df_merged)
    
        
    alert_manager.volumePositive(df_merged)
    alert_manager.volumeNegative(df_merged)
    
    
    crossover_manager.smacrossovers(df_merged)
    crossover_manager.macd_crossovers(df_merged)
    crossover_manager.obos_alerts(df_merged)
    
    
    
    dbdao.save_dataframe(df_merged, "df_history")
   
    
        
    #alert_manager.relative_strength(df_merged, df_spy, symbol)

    
    
    
    
    df_merged['stdabove_prev']=df_merged['stdabove'].shift(1)
    
    #latest data calculations
    return_data={}
    
    return_data.update(calculate_beta(df_symbol_close,df_mkt_close,symbol))
    
    
    return_data.update(  calculate_prices_at_dates(df_symbol_close,hist_dates))
    
    monthly_date = hist_dates['Monthly']
    weekly_date = hist_dates['Weekly']
    
    df_latest=df_merged.tail(1) 
    
    df_latest_sign=df_latest.apply(calc_signs,axis=1)
    
    df_latest=pd.concat([df_latest,df_latest_sign],axis=1)
    
    #df_latest[['sma_20day_sign']]=df_latest.apply(calc_signs,axis=1)
    df_latest['volatility_monthly']= price_manager.get_specific_date_value(df_merged,monthly_date,'volatility')
    df_latest['volatility_weekly']= price_manager.get_specific_date_value(df_merged,weekly_date,'volatility')
    df_latest['std50days']=df_latest['stdabove']
    df_latest['date']=df_latest.index
    df_latest.set_index('date',inplace=True)
    
        
    
    
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




    