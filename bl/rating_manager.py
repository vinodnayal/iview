import talib
from talib import abstract
from talib import MA_Type
import numpy as np
from talib import abstract


import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
from util import loglib
from util import constants
import math
from bl import price_manager as pricing
from datetime import timedelta



def rating_calculation(date_150,date_50,date_21,df,date_calculation,symbol):
    
    date_150_data=pricing.get_specific_date_value(df, date_150,'close')
    date_50_data=pricing.get_specific_date_value(df, date_50,'close')
    date_21_data=pricing.get_specific_date_value(df, date_21,'close')
    latest_data=pricing.get_specific_date_data(df, date_calculation)
    
    long_term_rating=30*(latest_data['close']-latest_data['sma200'])/(latest_data['sma200'])
    +            30*(latest_data['close']-date_150_data)/(date_150_data)
    
    medium_term_rating=15*(latest_data['close']-latest_data['sma100'])/(latest_data['sma100'])
    +            15*(latest_data['close']-date_50_data)/(date_50_data)
    
    short_term_rating=5*(latest_data['close']-latest_data['sma20'])/(latest_data['sma20'])
    +            5*(latest_data['close']-date_21_data)/(date_21_data)
    
    rating=long_term_rating+medium_term_rating+short_term_rating
    
    return rating
             
    




def calc_rating_history(df_merged,days_behind,symbol):
    
    df=df_merged[['sma200', 'sma100','sma20','close']]
    end_date = datetime.datetime.now()
    history_start_date=(end_date - relativedelta(days=days_behind))
    df_rating = pd.DataFrame(columns=('date','rating','symbol'))
    
    for x in range(0,days_behind):
        
            date_calculation= (history_start_date + relativedelta(days=x))
            date_150 = (date_calculation - relativedelta(days=150)).date()
            date_50 = (date_calculation - relativedelta(days=50)).date()
            date_20=(date_calculation - relativedelta(days=20)).date()
            date_calculation=date_calculation.date()
            
            rating=rating_calculation(date_150,date_50,date_20,df,date_calculation,symbol)
            
            df_rating.loc[x]=(date_calculation,rating,symbol)
            
    #print df_rating
    df_rating= df_rating.set_index('date')
    return df_rating
    
