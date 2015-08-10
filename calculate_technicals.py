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
    base_path="data/"
    list_symbol=dbdao.get_symbols_list()
   
    df_mkt=mongodao.getsymbol_data(constants.MKT_SYMBOL, start_date_time, end_date_time)
    
    df_technicals = technical_manager.calculate_technical(df_mkt,constants.MKT_SYMBOL,df_mkt, start_date_time, end_date_time, base_path)
    
    frames=[df_technicals]
    for symbol in list_symbol:    
        try:
            df_symbol=mongodao.getsymbol_data(symbol, start_date_time, end_date_time)
                   
            if df_symbol.empty:
                return
            
            
            logger.info("Getting Technicals for symbol=%s ",symbol)
            df_technicals_new = technical_manager.calculate_technical(df_symbol,symbol,df_mkt, start_date_time, end_date_time, base_path)
            frames.append(df_technicals_new)
            #
            logger.info("Got Technicals for symbol=%s ",symbol)
        except Exception ,ex:
            logger.error(ex)
    
    
    print frames
    result = pd.concat(frames)  
    print result
    dbdao.save_dataframe(result,"df_technicals");


calculate_technicals()



