import urllib2
from BeautifulSoup import BeautifulSoup
import re
import pandas as pd
from dao import dbdao
from util import loglib

logger = loglib.getlogger('active_news')


def get_csv():
    try:
        #url=url.replace('html','csv')    
        url="http://www.nasdaq.com/markets/most-active.aspx"
        
        
       
        page = urllib2.urlopen(url,timeout = 10)
        html = page.read()
        soup = BeautifulSoup(html)
        symbols=[]
        for  y in soup.findAll('table'):
            for td in y.findAll('td'):
                h3=td.find('h3')
                if(h3):
                    symbols.append( {"symbol":h3.text.strip()})
            #anchors = [a.text for a in (td.find('h3') for td in y.findAll('td')) if a]
        print symbols
        df=pd.DataFrame(symbols)
        df.set_index("symbol",inplace=True)
        dbdao.execute_query(["delete from news_top_symbols"])
        dbdao.save_dataframe(df, "news_top_symbols")
    except Exception ,ex:
        logger.error(ex)
        

get_csv()