
from talib import abstract


import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd

from util import loglib, alert_constants

from util import constants

from bl import  crossover_manager, rsi_manager, alert_manager, trend_manager
from dao import mongodao, dbdao
import math




end_date_time = datetime.datetime.now()  # mysqldb.get_maxdate()[0]   
start_date_time = end_date_time - relativedelta(days=constants.DAYS_FOR_TECHNICALS)
    
df_mkt=mongodao.getSymbolDataWithSymbol("SPY", start_date_time, end_date_time)  

symbol="MSFT"
df_symbol=mongodao.getSymbolDataWithSymbol(symbol, start_date_time, end_date_time)  

df_symbol_close = df_symbol[['close']]

df_mkt_close = df_mkt[['close']]
mom=abstract.MOM(df_symbol_close, timeperiod=5)
df_merged=abstract.MACD(df_symbol_close,fastperiod=12,slowperiod=26,signalperiod=9)
   
#df_merged=macd.apply(np.round)

df_std= abstract.STDDEV(df_symbol_close.pct_change(),timeperiod=100)
df_merged['stddev']=df_std
df_merged['volatility']=df_std*100*math.sqrt(252)
rsi=abstract.RSI(df_symbol_close).round(2)

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



df_trends=df_merged.apply(lambda row : trend_manager.trend_calculation(row),axis=1)

df_merged=pd.concat([df_merged,df_trends],axis=1)


crossover_manager.TrendChangePositive(df_merged,"short_trend",alert_constants.TREND_SHORT)
crossover_manager.TrendChangePositive(df_merged,"inter_trend",alert_constants.TREND_INTERMEDIATE)
crossover_manager.TrendChangePositive(df_merged,"long_trend",alert_constants.TREND_LONG)


crossover_manager.TrendChangeNegative(df_merged,"short_trend",alert_constants.TREND_SHORT)
crossover_manager.TrendChangeNegative(df_merged,"inter_trend",alert_constants.TREND_INTERMEDIATE)
crossover_manager.TrendChangeNegative(df_merged,"long_trend",alert_constants.TREND_LONG)







