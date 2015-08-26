import urllib2
import pandas
import numpy as np
from dao import dbdao

from util import loglib
from boto.ec2.volume import Volume
logger = loglib.getloggerWithFile('livedataimport','livedataimport.txt')


def parseStr(s):
    ''' convert string to a float or string '''
    f = s.strip()
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
        
def saveQuote(symbols):
    
    ''' get current yahoo quote, return a DataFrame  '''
    # for codes see: http://www.gummy-stuff.org/Yahoo-data.htm
    if not isinstance(symbols,list):
        symbols = [symbols]
    
    
    header =['yield','dividend','ex_dividend_date','market_cap','market_cap_realtime','float_shares','short_ratio','peg_ratio','revenue','price_sales','price_book',
             'book_value','earning_per_share','avg_daily_volume','name','symbol','last','price_change','change_pct','PE','time','prev_close','eps','market_cap','52weeklow','52weekhigh','volume']
    
    
    keys=['y','d','q','j1','j3','f6','s7','r5','s6','p5','p6','p4','e','a2','n','s',     'l1', 'c1',    'p2'  ,   'r', 't1', 'p',       'e'     , 'j1','j','k','v']    
    request = str.join('',keys )
    
    print len(header)
    print len(keys)
    
    #data = dict(zip(header,[[] for i in range(len(header))]))
    list_data=[]
    urlStr = 'http://finance.yahoo.com/d/quotes.csv?s=%s&f=%s' % (str.join('+',symbols), request)
    #logger.info(urlStr)
    try:
        lines = urllib2.urlopen(urlStr,timeout = 10).readlines()
        for line in lines:
            fields = line.strip().split(',')
            data={}
            for i,field in enumerate(fields):
                data[header[i]]=parseStr(field)
            list_data.append(data)
        df=pandas.DataFrame(list_data)
        df=df.fillna(0)
        
        dbdao.save_dataframe(df,'symbol_live_yahoo')
        
    except Exception, e:
        s = "Failed to download:\n{0}".format(e);
        logger.error(s)
        exit()
        
        
def getdataforall_list( list_symbols):
        
        
        
        for i in range(0, len(list_symbols), 40):
            chunk = list_symbols[i:i + 40]    
            logger.info( chunk)    
            saveQuote(chunk)
            
           
           
getdataforall_list(['MSFT','AAPL']) 