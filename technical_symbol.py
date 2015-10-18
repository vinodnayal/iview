import numpy
import talib
from talib import MA_Type
import numpy as np
from talib import abstract
from dao import dbdao,mongodao

import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd

from util import loglib

import csv
from util import constants
import os
from bl import technical_manager


logger = loglib.getlogger('technicals')


def calculate_technicals(start,end):
    
    end_date_time = datetime.datetime.now()  # mysqldb.get_maxdate()[0]   
    start_date_time = end_date_time - relativedelta(days=constants.DAYS_FOR_TECHNICALS)
    
    list_symbol=dbdao.get_symbols_list_limit(start,end)
    
    hist_dates= dbdao.get_historical_dates()
    
    
   
    
    days_behind=1
    
    df_mkt=mongodao.getsymbol_data(constants.MKT_SYMBOL, start_date_time, end_date_time)
    
    print df_mkt
    
    if(start=='0'):        
        dbdao.execute_query(["delete from df_technical","delete from df_history"])
    df_technicals = technical_manager.calculate_technical(df_mkt,constants.MKT_SYMBOL,df_mkt, start_date_time, end_date_time, hist_dates,days_behind)
    
    frames=[df_technicals]
    for symbol in list_symbol:    
        try:
            df_symbol=mongodao.getsymbol_data_temp(symbol, start_date_time, end_date_time)
            
            if df_symbol.empty:
                continue
            
            
            logger.info("Getting Technicals for symbol=%s ",symbol)
            df_technicals_new = technical_manager.calculate_technical(df_symbol,symbol,df_mkt, start_date_time, end_date_time, hist_dates,days_behind)
            
            
            frames.append(df_technicals_new)
            
            logger.info("Got Technicals for symbol=%s ",symbol)
        except Exception ,ex:
            logger.error(ex)
    
    
    
    result = pd.concat(frames)  
    
    dbdao.save_dataframe(result,"df_technical");
    sql_max_min_median_5days = open('queries/high_low_median.sql', 'r').read()
    sql_relative = open('queries/relative_strength.sql', 'r').read()  
    sql_update_technical_history = open('queries/update_technical_history.txt', 'r').read()  
    logger.info("Executing Queries for updating technicals")
    dbdao.execute_query([sql_max_min_median_5days,sql_relative,sql_update_technical_history])
    logger.info("Queries Completed !")
    

import sys
print sys.argv
start,end=sys.argv[1],sys.argv[2]
calculate_technicals(start,end)



