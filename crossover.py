import talib as ta
import numpy
from talib import abstract
import talib
from talib import MA_Type
import numpy as np
from talib import abstract
from dao import dbdao,mongodao

import dao.mongodao as mongodao
import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd

from util import loglib

import csv
from util import constants
import os
from bl import technical_manager, crossover_manager

end_date_time = datetime.datetime.now()  # mysqldb.get_maxdate()[0]   
start_date_time = end_date_time - relativedelta(days=constants.DAYS_FOR_TECHNICALS)
    

    
df=mongodao.getsymbol_data_temp("MSFT", start_date_time, end_date_time)    
list_drop_cloumns = [ 'open', 'high','low']

df = df.drop(list_drop_cloumns,1)

sma25 = abstract.SMA(df, timeperiod=25).round(2)
     
sma50 = abstract.SMA(df, timeperiod=50).round(2)
 
df_merged=df
df_merged['sma25']=sma25
df_merged['sma20']=sma50
 
 
crossover_manager.give_positive_co_dates(df_merged,'sma25','sma20')
 
 
crossover_manager.give_negative_co_dates(df_merged,'sma25','sma20')




macd = abstract.MACD(df,fastperiod=8,slowperiod=17,signalperiod=9)

crossover_manager.bullish_co(macd, 'macdhist')
crossover_manager.bearish_co(macd, 'macdhist')
# 
# print macd




