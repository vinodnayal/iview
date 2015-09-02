import urllib2
from BeautifulSoup import BeautifulSoup
from dao import dbdao
import os
import pandas as pd
from util import df_util, loglib


logger = loglib.getlogger('symbol_holding')


def get_holdings(symbol):
    url='http://finance.yahoo.com/q/hl?s='+symbol+'+Holdings'
    print url
    page=urllib2.urlopen(url,timeout=10)
    soup=BeautifulSoup(page)
    filepath="data/holdings/"+symbol+".csv"
    f1=open(filepath,"w")
    columns="Symbol^holding_company^holding_symbol^holding_pct"
    f1=open(filepath,'w')
    f1.write(columns)
    f1.write("\n")
        
    
    all_tables=soup.findAll('table',attrs={"class":"yfnc_tableout1"})
    if(len(all_tables)>1):
        holdings= all_tables[0].findAll('td',attrs={"class":"yfnc_tabledata1"})
        count=0
        list_holding=[]
        
        for holding in holdings:
            list_holding.append(holding.text)
            
            if(count==2):
                count=-1  
                f1.write(symbol+'^')                                       
                f1.write(("^").join(list_holding))
                f1.write("\n")
                list_holding=[]
                                  
            count=count+1
    f1.close()
    

def yf_get_key_stat(SYM):
    
    url='http://finance.yahoo.com/q/hl?s='+SYM+'+Holdings'
   
    page=urllib2.urlopen(url,timeout=10)
    print url
    
    html = page.read()
    soup = BeautifulSoup(html)
    
#     res = [[x.text for x in y.parent.contents] for  y in soup.findAll('td', attrs={"class" : "yfnc_tabledata1"})]
#     print res
    header=["holding_company","holding_symbol","holding_pct","ytd"]
    count=0
    y =soup.findAll('table', attrs={"class" : "yfnc_tableout1"})
    rows= y[0].findAll('tr')
    for row in rows:
        print row
        tds= row.findAll('td', attrs={"class" : "yfnc_tabledata1"})
        print tds
        count=0
        dict={}
        for td in tds:
            print td.text
          #  print count
            #dict[header[count]]=td.text
            count=count+1
            print td.text
        print dict
    #print y.parent.parent.childrens  
#         length= len(y.parent.parent.contents)
#         if(length<4):
#             break;
#         
#         print y.text
#         for x in y:
#             print x.text
        
    
    #return res

print yf_get_key_stat('ABMIX')
# list_symbol=dbdao.get_etf_symbols()
# for symbol in list_symbol:
#     try:
#         get_holdings(symbol)
#     except Exception,ex:
#         logger.error(ex)
    
# df=df_util.create_dataframe("data/holdings/", "Symbol")
# print df
# dbdao.save_dataframe(df, "symbol_holdings")
    
    