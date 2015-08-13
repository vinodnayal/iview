import numpy
import talib
from talib import MA_Type
import numpy as np
from talib import abstract
import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
from util import loglib
import csv
from util import constants
import os
from dao import mongodao
from dao import dbdao
from bl import rating_manager

logger = loglib.getlogger('rating')
def symbol_rating_calc(days_behind):
    
    end_date_time = datetime.datetime.now()  # mysqldb.get_maxdate()[0]   
    start_date_time = end_date_time - relativedelta(days=700)
         
    list_symbol=dbdao.get_symbols_list()
    
    
    df_mkt=mongodao.getsymbol_data_temp(constants.MKT_SYMBOL, start_date_time, end_date_time)
    
    for symbol in list_symbol:    
        try:
            df_symbol=mongodao.getsymbol_data_temp(symbol, start_date_time, end_date_time)
                   
            if df_symbol.empty:
                return
            logger.info("Getting Rating for symbol=%s ",symbol)
            
    
            df_result=rating_manager.symbol_rating_calculation(df_symbol,symbol,df_mkt, start_date_time, end_date_time,days_behind)
            print df_result
            logger.info("Got Rating for symbol=%s ",symbol)
        
        except Exception ,ex:
            logger.error(ex)
            


symbol_rating_calc(10)