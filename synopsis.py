from dao2 import dbdao
import pandas as pd
from bl import Trend_types
df= dbdao.get_data_db_frame("select symbol,short_trend,inter_trend,long_trend,rsi_value from df_technical where symbol='MSFT';")



def sypnosis(x):
    print x
    rsi_value=x['rsi_value']
    symbol=x['symbol']
    short_trend= Trend_types.getString(x['short_trend'])
    inter_trend=Trend_types.getString(x['inter_trend'])
    long_trend=Trend_types.getString(x['long_trend'])
    current_situation=""
    
    current_situation= "%s short term is %s , intermediate term is %s , and  long term is %s , %s is %s" %(symbol,short_trend,inter_trend,long_trend,symbol,rsi_value)
    
    #return short_trend,inter_trend,long_trend,current_situation
    return pd.Series({'short_trend_text': short_trend, 'inter_trend_text': inter_trend,'long_trend_text':long_trend,'current_situation': current_situation})


df=df.merge(df.apply(sypnosis,axis=1),left_index=True, right_index=True)
print df
dbdao.save_dataframe(df, "df_synopsis")