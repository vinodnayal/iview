
from util import  constants
import talib
from talib import MA_Type
import numpy as np
from talib import abstract
import math
import matplotlib.pyplot as plt



def calculate_beta_std(df,df_mkt,symbol):
    
    
    
    df = df.rename(columns={constants.CLOSE: constants.MKT_SYMBOL})
    df_mkt = df_mkt.rename(columns={constants.CLOSE: symbol})[symbol]
    df_merged = df.join(df_mkt)
    print df_merged[0:5]
    
    returns = df_merged.pct_change()
    stddev= returns.std()[symbol]
    volatility= stddev* 100 * math.sqrt(252)
    variance = returns.var() 
    covariance = returns.cov()
    beta = covariance.loc[symbol, constants.MKT_SYMBOL] / variance.loc[constants.MKT_SYMBOL]
    return {"beta":beta,"stddev":stddev,"volatility":volatility}
    
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



def calculate_technical(df_symbol,symbol,df_mkt,start_date_time,end_date_time,base_path): 
    
    list_drop_cloumns = [ 'open', 'high','low']
    df_symbol_close = df_symbol.drop(list_drop_cloumns,1)
    df_mkt_close = df_mkt.drop(list_drop_cloumns,1)
    
    return_data={}
    return_data.update(calculate_beta_std(df_symbol_close,df_mkt_close,symbol))
    return_data.update( calculate_res_sup(df_symbol))
    print return_data
    exit()
    filepath=base_path+"/"+symbol+'.csv'   
    df_temp=df_symbol_close.pct_change()
#    print df_temp.std()
    mom=abstract.MOM(df_symbol_close, timeperiod=5)
    #stddev=abstract.STDDEV(df_temp)
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
    #df_merged['stddev']=stddev
    df_merged['close']=df_symbol_close
    df_merged=df_merged.dropna()
    df_merged['symbol']=symbol
    #df_merged['volatility']=df_merged.apply(calc_Volatility, axis=1 )
    df_merged['rsi_value'] = df_merged['rsi'].apply(calculate_rsi_values )
    df_plot=df_merged[['stddev']]
    df_plot.plot()
    plt.show()
    
    """
    
    df_merged['rsi_value_shifted']=df_merged['rsi_value'].shift(1)
    df_merged['rsi_value_change']=df_merged['rsi_value']-df_merged['rsi_value_shifted']
    df_change_history=df_merged[df_merged['rsi_value_change']!=0][['rsi','rsi_value','rsi_value_shifted']]
    df_merged['sma200_price_diff']=df_merged['close']-df_merged['sma200']
    df_merged['sma200_price_diff_shifted']=df_merged['sma200_price_diff'].shift(1)
    df_merged['sma200_price_co'] = df_merged.apply(calculate_sma_co,axis=1 )
    df_change_history=df_merged[df_merged['sma200_price_co']>0][['sma200','close']]

    """
    
    df_merged.to_csv(filepath,sep=",")


    
    



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
    