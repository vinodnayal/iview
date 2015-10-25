
from talib import abstract


import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd

from util import loglib, alert_constants

from util import constants

from bl import  crossover_manager, rsi_manager, alert_manager
from dao import mongodao, dbdao


    
end_date_time = datetime.datetime.now()  # mysqldb.get_maxdate()[0]   
start_date_time = end_date_time - relativedelta(days=constants.DAYS_FOR_TECHNICALS)
    
df_spy=mongodao.getSymbolDataWithSymbol("SPY", start_date_time, end_date_time)  

symbol="MSFT"
df=mongodao.getSymbolDataWithSymbol(symbol, start_date_time, end_date_time)  

df['sma_volume_6month']= pd.rolling_mean(df['volume'], window=120).round(2)
df=df.dropna()

dbdao.execute_query(["truncate df_alerts"])

#six_month_return =df[['close']].apply(lambda x: x- x.shift(120))

alert_manager.fullGapPositive(df)
alert_manager.fullGapNegative(df)
alert_manager.partialGapPositive(df)
alert_manager.partialGapNegative(df)
alert_manager.keyReversalPositive(df)
alert_manager.keyReversalNegative(df)
alert_manager.volumePositive(df)
alert_manager.volumeNegative(df)
alert_manager.relative_strength(df, df_spy, symbol)


