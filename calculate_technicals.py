import numpy
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
from bl import technical_manager


logger = loglib.getlogger('technical_indicators')


def calculate_technicals():
    
    end_date_time = datetime.datetime.now()  # mysqldb.get_maxdate()[0]   
    start_date_time = end_date_time - relativedelta(days=constants.DAYS_FOR_TECHNICALS)
    
    list_symbol=dbdao.get_symbols_list()
    
    hist_dates= dbdao.get_historical_dates()
    
    
   
    
    days_behind=100
    
    df_mkt=mongodao.getsymbol_data_temp(constants.MKT_SYMBOL, start_date_time, end_date_time)
    
    dbdao.execute_query(["delete from df_technicals"])
    df_technicals = technical_manager.calculate_technical(df_mkt,constants.MKT_SYMBOL,df_mkt, start_date_time, end_date_time, hist_dates,days_behind)
    
    frames=[df_technicals]
    for symbol in list_symbol:    
        try:
            df_symbol=mongodao.getsymbol_data_temp(symbol, start_date_time, end_date_time)
            
            if df_symbol.empty:
                return
            
            
            logger.info("Getting Technicals for symbol=%s ",symbol)
            df_technicals_new = technical_manager.calculate_technical(df_symbol,symbol,df_mkt, start_date_time, end_date_time, hist_dates,days_behind)
            
            
            frames.append(df_technicals_new)
            
            logger.info("Got Technicals for symbol=%s ",symbol)
        except Exception ,ex:
            logger.error(ex)
    
    
    
    result = pd.concat(frames)  
    
    dbdao.save_dataframe(result,"df_technicals");
    f_max_min_median_5days = open('queries/high_low_median.sql', 'r')
    sql_max_min_median_5days= f_max_min_median_5days.read()
    
    f_relative = open('queries/relative_strength.sql', 'r')
    sql_relative= f_relative.read()

    dbdao.execute_query([sql_max_min_median_5days,sql_relative])
calculate_technicals()



