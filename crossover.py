
from talib import abstract


import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd

from util import loglib, alert_constants

from util import constants

from bl import  crossover_manager, rsi_manager
from dao import mongodao, dbdao

def fullGapPositive(df):
    diff=df['open']>df['high'].shift(1)
    df= df[diff]
    df['sign']=1
    df['typeid']=alert_constants.Full_Gap_Up
    print df
    

def fullGapNegative(df):
    diff=df['open']<df['low'].shift(1)
    df= df[diff]
    df['sign']=-1
    df['typeid']=alert_constants.Full_Gap_Down
    print df

def partialGapPositive(df):
    diff=df['open']>df['close'].shift(1)
    df= df[diff]
    df['sign']=1
    df['typeid']=alert_constants.Partial_Gap_up
    print df
    
def partialGapNegative(df):
    diff=df['open']<df['close'].shift(1)
    df= df[diff]
    df['sign']=-1
    df['typeid']=alert_constants.Partial_Gap_Down
    print df    

    
end_date_time = datetime.datetime.now()  # mysqldb.get_maxdate()[0]   
start_date_time = end_date_time - relativedelta(days=constants.DAYS_FOR_TECHNICALS)
    

symbol="MSFT"
df=mongodao.getsymbol_data(symbol, start_date_time, end_date_time)  

df['sma_volume_6month']= pd.rolling_mean(df['volume'], window=120).round(2)
df=df.dropna()
print df
exit()

fullGapPositive(df)
fullGapNegative(df)
partialGapPositive(df)
partialGapNegative(df)






