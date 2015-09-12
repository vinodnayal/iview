from util import loglib
import os
import urllib2
from xml.dom import minidom
from BeautifulSoup import BeautifulSoup
import urllib2
import pandas as pd
import csv
from IPython.core.page import page
from dao import dbdao

def get_holdings(symbol):
    url='http://finance.yahoo.com/q/hl?s='+symbol+'+Holdings'
    print url
    page=urllib2.urlopen(url,timeout=10)
    soup=BeautifulSoup(page)
   
    all_tables=soup.findAll('table',attrs={"class":"yfnc_tableout1"})
    list_data=[]
    if(len(all_tables)>1):
        holdings= all_tables[0].findAll('tr')
        for holding in holdings[1:]:
            #print holding
            items= holding.findAll('td',attrs={"class":"yfnc_tabledata1"})
            if(len(items)>=3):
                data =    {"symbol":symbol,"holding_company":items[0].text,"holding_symbol":items[1].text,"holding_pct":items[2].text} 
                #print data
                list_data.append(data)
#         

        df=pd.DataFrame(list_data)
        df.set_index("symbol",inplace=True)
        print df 
        dbdao.save_dataframe(df, "symbol_holdings")
list_symbol=dbdao.get_etf_symbols()
for symbol in list_symbol: 
    try:
        get_holdings(symbol)
    except Exception,ex:
        print ex
    
    
    
    