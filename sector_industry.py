import urllib2
from BeautifulSoup import BeautifulSoup
import re
import pandas as pd
from dao import dbdao
from util import loglib

logger = loglib.getlogger('sector_industry')

def get_csv(url):
    try:
        #url=url.replace('html','csv')    
        base_url="http://biz.yahoo.com/p/"
        
        url=base_url+url
        print url
       
        page = urllib2.urlopen(url,timeout = 10)
        html = page.read()
        soup = BeautifulSoup(html)
        sector=""
        industry=""
        list_symbol=[]
        for  y in soup.findAll('table' ,attrs={"bgcolor" : "dcdcdc"}):
            for x in  y.findAll('td',attrs={"bgcolor" : "ffffee"}):
               
                if("Sector:" in x.text ):
                    sector=x.text.replace("Sector:","")
                elif("Industry:" in x.text ):
                    industry=x.text.replace("Industry:","").replace("(More Info)","")
                else:
                    name= x.text.replace("\n","").replace("\r","")
                    items_symbol= re.findall('([\w\s.]+)',name)
                    if(items_symbol is not None and len(items_symbol) >=2):
                        symbol=items_symbol[1]
                        name=items_symbol[0]
                        print name
                        print symbol
                        list_symbol.append({"name":name,"symbol":symbol})
                    
        
        print sector
        print industry
        
        df=pd.DataFrame(list_symbol)
        df.set_index('symbol',inplace=True)
        df['sector']=sector
        df['industry']=industry
        print df
        dbdao.save_dataframe(df, "df_symbol_latest")
    except Exception ,ex:
        logger.error(ex)
        
    


def get_items(url):
    page = urllib2.urlopen(url,timeout = 10)
    html = page.read()
    searchObj = re.findall( r'\d+conameu.html', html)
    return searchObj
    

def getsymbol_sector_industry():
   
    #re.compile("*.html")
    base_url="http://biz.yahoo.com/p/"
    url = base_url+"s_conameu.html"
    url_list= get_items(url)
    for url_industry in url_list:
        url_industry=  base_url+url_industry
        print url_industry
        url_csv_list= get_items(url_industry)
        for url_csv in url_csv_list:
            print url_csv
            get_csv(url_csv)
    
    
    
   
    
    
   
        
#url="http://biz.yahoo.com/p/811conameu.html"
#get_csv(url)
getsymbol_sector_industry()