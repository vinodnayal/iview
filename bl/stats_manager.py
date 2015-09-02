#from utils import loglib
#import os
from util import loglib
import urllib2
#from xml.dom import minidom
from BeautifulSoup import BeautifulSoup
#import urllib2
#from utils import loglib
#import csv
from dao import dbdao

logger = loglib.getlogger('stats_manager')

def create_files(filepath,symbol,url):
    
    try:
    
        page=urllib2.urlopen(url,timeout=10)
        soup=BeautifulSoup(page)
        
        columns="Symbol^Item^q1^q2^q3^q4"
        f1=open(filepath,'w')
        f1.write(columns)
        f1.write("\n")
        all_tables=soup.findAll('table',attrs={"class":"yfnc_tabledata1"})
        
        for data in all_tables:
            all_data= data.findAll('tr')
            header=[]
            header.append(symbol)
            count=0
            for rows in all_data:
                if count==0:
                    for s in rows:
                        y= s.findAll('tr',attrs={"class":"yfnc_modtitle1"})
                        for u in y:
                            title=u.findAll('td')
                            for e in title:
                                header.append(e.text)
                                head=""
                                for t in u.findAll('th'): 
                                    data= t.text.replace('&nbsp;','')
                                    if(data !=''):
                                        header.append(data)
                                        head="^".join(header)
                                        
                                if(head !="" ):
                                    f1.write(head)
                                #print head
                                f1.write('\n')
                    
                count=count+1
                if (count ==1):
                    continue                   
                columns= rows.findAll('td')
                linedata=[]
                linedata.append(symbol)
                if(len(columns)<3):
                    continue
                
                headers=["Symbol","Item","q1","q2","q3","q4"]
                dict={}
                count=0
                for column in columns:
                    value=column.text.replace('&nbsp;','').replace('\n','')
                    #dict[headers[]]
                    count=count+1
                    if('-' not in value and  value!=''):
                        linedata.append(value)
                        line="^".join(linedata)
                if(len(linedata)>3):                
                    f1.write(line)
                    #print line
                    f1.write('\n')
                
        f1.close()
    except Exception,ex:
        logger.error(ex)


def get_IncomeStatement(symbol):
    url='http://finance.yahoo.com/q/is?s='+symbol
    print "get_IncomeStatement "+url
    filepath='data/stats/income_statement/'+symbol+".csv"
    create_files(filepath, symbol, url)
    
     
     
def get_BalanceSheet(symbol):
    
    url='http://finance.yahoo.com/q/bs?s='+symbol    
    filepath="data/stats/balance_sheet/"+symbol+".csv"
    print "get_BalanceSheet "+url
    create_files(filepath, symbol, url)    
   


def get_CashFlow(symbol):
    
    url='http://finance.yahoo.com/q/cf?s='+symbol
    filepath="data/stats/cash_flow/"+symbol+".csv"
    print "get_CashFlow "+url
    create_files(filepath, symbol, url)
    
def yf_get_key_stat(SYM):
    
    url = "http://finance.yahoo.com/q/ks?s=" + SYM + "+Key+Statistics"
    page=urllib2.urlopen(url,timeout=10)
    print url
    
    html = page.read()
    soup = BeautifulSoup(html)
    
    res = [[x.text for x in y.parent.contents] for  y in soup.findAll('td', attrs={"class" : "yfnc_tablehead1"})]
    
    return res