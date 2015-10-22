
from talib import abstract


import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd

from util import loglib

from util import constants

from bl import  crossover_manager, rsi_manager
from dao import mongodao, dbdao

end_date_time = datetime.datetime.now()  # mysqldb.get_maxdate()[0]   
start_date_time = end_date_time - relativedelta(days=constants.DAYS_FOR_TECHNICALS)
    

symbol="MSFT"
df=mongodao.getsymbol_data(symbol, start_date_time, end_date_time)    
list_drop_cloumns = [ 'open', 'high','low']

df = df.drop(list_drop_cloumns,1)
df['rsi']=abstract.RSI(df).round(2)

df_rsi=rsi_manager.obos_alerts(df)


dbdao.save_dataframe(df_rsi, "df_alerts")
   
# sma25 = abstract.SMA(df, timeperiod=25).round(2)
#      
# sma50 = abstract.SMA(df, timeperiod=50).round(2)
#  
# df_merged=df
# df_merged['sma25']=sma25
# df_merged['sma20']=sma50
#  
#  
# crossover_manager.give_positive_co_dates(df_merged,'sma25','sma20')
#  
# 
# crossover_manager.give_negative_co_dates(df_merged,'sma25','sma20')




macd = abstract.MACD(df,fastperiod=12,slowperiod=26,signalperiod=9)

df_bull_signal= crossover_manager.bullish_co(macd, 'macdhist',1)
df_bull_signal['symbol']=symbol

df_bear_signal=crossover_manager.bearish_co(macd, 'macdhist',2)
df_bear_signal['symbol']=symbol






df_bull_center= crossover_manager.bullish_co(macd, 'macd',3)
df_bull_center['symbol']=symbol


df_bear_center=crossover_manager.bearish_co(macd, 'macd',4)
df_bear_center['symbol']=symbol


list_drop_cloumns = [ 'macd', 'macdsignal','macdhist']
# df_macdcoll=[df_bull_signal,df_bear_signal,df_bull_center,df_bear_center]
# df_macdcoll_sel_columns=[]
# for df in df_macdcoll:
#     df = df.drop(list_drop_cloumns,1)
#     df_macdcoll_sel_columns.append(df)
    

df_merged=pd.concat([df_bull_signal,df_bear_signal,df_bull_center,df_bear_center],axis=0)
df_merged=df_merged.drop(list_drop_cloumns,1)

dbdao.save_dataframe(df_merged, "df_alerts")




