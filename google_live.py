import urllib2
from BeautifulSoup import BeautifulSoup
import re
import pandas as pd
from dao import dbdao
from util import loglib
import json

logger = loglib.getlogger('google_live')


def getgoogledata(list_symbol):
    
    symbols = str.join(',',list_symbol)        
    url = 'http://finance.google.com/finance/info?q=%s' % symbols
    print url
    page = urllib2.urlopen(url,timeout = 10)
    html = page.read().replace("//","").strip()
    data  = json.loads(html)
     
    df=pd.DataFrame(data)
    df.set_index('t',inplace=True)
    return df


dbdao.execute_query(['delete from google_live_indices_symbol','delete from google_live_symbol'])
list_symbol=dbdao.get_indices_symbols_list()

df=getgoogledata(list_symbol)

dbdao.save_dataframe(df, "google_live_indices_symbol")


list_symbol=dbdao.get_symbols_list()
for i in range(0, len(list_symbol), 40):
    try:
                chunk = list_symbol[i:i + 40]
                df=getgoogledata(chunk)
                dbdao.save_dataframe(df, "google_live_symbol")    
                logger.info( chunk)   
    except Exception,ex:
        logger.error(ex)

sql_update=""" update live_symbol t1 , google_live_symbol t2
            set price_change=t2.c_fix,
            change_pct=cp_fix,
            last=l_fix
            where t1.symbol=t2.t"""


sql_indices_update=""" update live_symbol t1 , google_live_indices_symbol t2,indices_symbol t3
    set price_change=t2.c_fix,
    change_pct=cp_fix,
    last=l_fix
    where t1.symbol=t3.symbol
    and ( t2.t=t3.googSymbol  or concat(t2.e,":",t2.t)=t3.googSymbol)"""
sql_goog_only="""insert into live_symbol(symbol,price_change,change_pct,last)
                select distinct t,
                c_fix,
                cp_fix,
                l_fix from google_live_symbol t1 
                left join live_symbol t2 
                on t1.t=t2.symbol
                where t2.symbol is null;"""

sql_indices=""" insert into live_symbol(symbol,price_change,change_pct,last)
                select 
                t3.symbol,
                c_fix,
                cp_fix,
                l_fix                
                 from  google_live_indices_symbol t2
                 left join indices_symbol t3 
                 on ( t2.t=t3.googSymbol  or concat(t2.e,":",t2.t)=t3.googSymbol)
                left join live_symbol t1 
                on t1.symbol=t3.symbol
                where t1.symbol is null                
                
                """

dbdao.execute_query([sql_update,sql_indices_update])
