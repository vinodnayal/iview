from datetime import timedelta
from pandas.io.data import DataReader
 
from MyConfig import MyConfig as cfg

from util import loglib
import urllib2
from BeautifulSoup import BeautifulSoup
import pandas as pd
from dao import dbdao
logger = loglib.getlogger('historicaldataimport')
url="http://stockcharts.com/freecharts/adjusthist.php?search=*"
#url="http://stockcharts.com/freecharts/adjusthist.php?search=*&day=-120"
headers = { 'User-Agent' : 'Mozilla/5.0' }
req = urllib2.Request(url, None, headers)
page = urllib2.urlopen(req,timeout=10)
# print page.read()
# exit()
soup=BeautifulSoup(page)
        
list_symbol=[]
all_tables=soup.findAll('table')
for table in all_tables:
    
    for tr in table.findAll('tr'):
        count=0
        tds=tr.findAll('td')
        dict_symbol={}
        if(len(tds)>=2):
             
            
                  
            dict_symbol.update({"symbol":tds[2].text})    
            dict_symbol.update({"date":tds[1].text})
        list_symbol.append(dict_symbol)

df= pd.DataFrame(list_symbol)
dbdao.save_dataframe(df, "df_splits")


#dataimport.specificimport(list_symbol)

