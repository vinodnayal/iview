import urllib2
from BeautifulSoup import BeautifulSoup
import pandas as pd
from dao import dbdao
from util import loglib
import finsymbols



logger = loglib.getlogger('symbols')

def get_all_symbols():
    
    sp500 = finsymbols.get_sp500_symbols()
    df_sp500=pd.DataFrame(sp500)
    df_sp500['exchange']='SPY500'
    
    amex_symbols=finsymbols.get_amex_symbols()
    df_amex=pd.DataFrame(amex_symbols)
    df_amex['exchange']='AMEX'
    
    
    
    
    nyse_symbols=finsymbols.get_nyse_symbols()
    df_nyse=pd.DataFrame(nyse_symbols)
    df_nyse['exchange']='NYSE'
    
    
    nasdaq_symbols=finsymbols.get_nasdaq_symbols()
    df_nasdaq=pd.DataFrame(nasdaq_symbols)
    df_nasdaq['exchange']='NASDAQ'
    
    
    result=pd.concat([df_sp500,df_amex,df_nyse,df_nasdaq])
    dbdao.save_dataframe(result, "df_symbol_new")
#     df=pd.DataFrame(sp500)
#     df.set_index("symbol",inplace=True)
#     dbdao.save_dataframe(df, "df_symbol_new")
#     print df

def getsymbol_sector_industry(SYM):
   
    url = "http://finance.yahoo.com/q/in?s="+SYM
    page = urllib2.urlopen(url,timeout = 10)
    print url
    
    html = page.read()
    soup = BeautifulSoup(html)
    
    res = [[x.text for x in y.parent.contents] for  y in soup.findAll('td', attrs={"class" : "yfnc_tabledata1"})]
    print res
    if(len(res)>1):
        industry=res[1][1].replace("amp;","").replace("\n","").replace("\r","")
        sector=res[0][1].replace("\n","").replace("\r","")
        return  {"symbol":SYM,"sector":sector,"industry":industry}
    else:
        return {"symbol":SYM,"sector":"","industry":""}

def create_sector_industry_data(start,end):
    list_symbol = dbdao.get_symbols_list_limit(start,end)
    list_symbol_data=[]
    for symbol in list_symbol:
        try:
            
            list_symbol_data.append(getsymbol_sector_industry(symbol))
        except Exception,ex:
            logger.error(ex)
            
        
        
    df=pd.DataFrame(list_symbol_data)
    df.set_index("symbol",inplace=True)
    dbdao.save_dataframe(df, "df_symbol_sector_industry")
    print df


import sys
print sys.argv
start,end=sys.argv[1],sys.argv[2]
print start,end
create_sector_industry_data(start,end)

#print getsymbol_sector_industry('XLV')




