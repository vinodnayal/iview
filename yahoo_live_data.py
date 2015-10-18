import urllib2
import pandas
import numpy as np
from dao import dbdao

from util import loglib
from boto.ec2.volume import Volume
logger = loglib.getloggerWithFile('yahoo_live_data','livedataimport.txt')


def parseStr(s):
    ''' convert string to a float or string '''
    f = s.strip().replace('\n','').replace('\r','')
    if f[0] == '"':
        return f.strip('"')
    elif f=='N/A':
        return np.nan
    
    else:
        try: # try float conversion
            prefixes = {'M':1e6, 'B': 1e9} 
            prefix = f[-1]
            
            if prefix in prefixes: # do we have a Billion/Million character?
                return float(f[:-1])*prefixes[prefix]
            else:                       # no, convert to float directly
                return float(f)
        except ValueError: # failed, return original string
            return s 
    
header =['yield','dividend','ex_dividend_date','market_cap','market_cap_realtime','float_shares','short_ratio','peg_ratio','revenue','price_sales','price_book',
             'book_value','earning_per_share','avg_daily_volume','symbol','last','price_change','change_pct','PE','time','prev_close',
             'eps','market_cap','52weeklow','52weekhigh','volume','name']
    
    
keys=['y','d','q','j1','j3','f6','s7','r5','s6','p5','p6','p4','e','a2','s',     'l1', 'c1',    'p2'  ,   'r', 't1', 'p',       'e'     , 'j1','j','k','v','n'] 
        
def saveQuote(symbols):
    

        if not isinstance(symbols,list):
            symbols = [symbols]
    
    
       
        request = str.join('',keys )
    
   
    
    #data = dict(zip(header,[[] for i in range(len(header))]))
        list_data=[]
        urlStr = 'http://finance.yahoo.com/d/quotes.csv?s=%s&f=%s' % (str.join('+',symbols), request)
        print urlStr
    #logger.info(urlStr)
#     try:
        lines = urllib2.urlopen(urlStr,timeout = 10).readlines()
        print lines
        for line in lines:
            #print line
            fields = line.strip().split(',')
            data={}
            #print fields
            if( len(fields) >27):
                fields[26]=fields[26]+fields[27]
            for i,header_name in enumerate(header):
                data[header_name]=parseStr(fields[i])
            list_data.append(data)
        df=pandas.DataFrame(list_data)
        df=df.fillna(0)
        
        dbdao.save_dataframe(df,'yahoo_live_symbol')
        
#     except Exception, e:
#         
#         logger.error(e)
#         exit()
        
        
        
def getdataforall_list( list_symbols):      
        
    try:   
        for i in range(0, len(list_symbols), 40):
            chunk = list_symbols[i:i + 40]    
            logger.info( chunk)    
            saveQuote(chunk)
    except Exception,ex:
        logger.error(ex)
                
        
            

dbdao.execute_query(["delete from yahoo_live_symbol"])           
list_symbol=dbdao.get_symbols_list()
getdataforall_list(list_symbol) 
update_sql=""" update live_symbol t1,yahoo_live_symbol t2
set 
t1.52weekhigh=t2.52weekhigh,
t1.52weeklow=t2.52weeklow,
t1.PE=t2.PE,
t1.avg_daily_volume=t2.avg_daily_volume,
t1.book_value=t2.book_value,
t1.change_pct=t2.change_pct,

t1.dividend=t2.dividend,
t1.eps=t2.eps,
t1.earning_per_share=t2.earning_per_share,
t1.ex_dividend_date=t2.ex_dividend_date,
t1.float_shares=t2.float_shares,
t1.last=t2.last,
t1.market_cap=t2.market_cap,
t1.peg_ratio=t2.peg_ratio,
t1.prev_close=t2.prev_close,
t1.price_change=t2.price_change,
t1.revenue=t2.revenue,
t1.short_ratio=t2.short_ratio,

t1.volume=t2.volume,
t1.yield=t2.yield
where t1.symbol=t2.symbol"""
dbdao.execute_query([update_sql])

#TODO update query
#dbdao.execute_query(["delete from live_symbol","insert into live_symbol select * from symbol_live_yahoo;"])