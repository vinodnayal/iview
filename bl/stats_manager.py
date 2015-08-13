#from utils import loglib
#import os
import urllib2
#from xml.dom import minidom
from BeautifulSoup import BeautifulSoup
#import urllib2
#from utils import loglib
#import csv
from dao import dbdao

def saveindb(filepath,symbol,url,type):
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
                            for t in u.findAll('th'): 
                                data= t.text.replace('&nbsp;','')
                                if(data !=''):
                                    header.append(data)
                                    head="^".join(header)
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
            for column in columns:
                value=column.text.replace('&nbsp;','').replace('\n','')
                if('-' not in value and  value!=''):
                    linedata.append(value)
                    line="^".join(linedata)
            if(len(linedata)>3):                
                f1.write(line)
                #print line
                f1.write('\n')
            
    f1.close()
    
    sql="""LOAD DATA LOCAL INFILE '%s'
        INTO TABLE fin_stats_symbol 
        FIELDS TERMINATED BY '^' 
        LINES TERMINATED BY "\n"
        IGNORE 1 LINES
        (@col1,@col2,@col3,@col4,@col5,@col6) set symbol=@col1,item=@col2,q1=@col3,q2=@col4,q3=@col5,q4=@col6,type=%s
        ;"""%(filepath,type)
    dbdao.execute_query([sql])
     

def get_IncomeStatement(symbol):
    url='http://finance.yahoo.com/q/is?s='+symbol
    filepath='data/stats/income_statement/'+symbol+".csv"
    saveindb(filepath, symbol, url,1)
    
     
     
def get_BalanceSheet(symbol):
    
    url='http://finance.yahoo.com/q/bs?s='+symbol    
    filepath="data/stats/balance_sheet/"+symbol+".csv"
    saveindb(filepath, symbol, url,2)    
   


def get_CashFlow(symbol):
    
    url='http://finance.yahoo.com/q/cf?s='+symbol
    filepath="data/stats/cash_flow/"+symbol+".csv"
    saveindb(filepath, symbol, url,3)