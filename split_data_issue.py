from dao import dbdao
from dao import mongodao
from dateutil.relativedelta import relativedelta
import datetime
import urllib2
from BeautifulSoup import BeautifulSoup
import pandas

url="http://stockcharts.com/freecharts/adjusthist.php?search=*"
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
        for td in tr.findAll('td'):
            if(count==2):
                list_symbol.append(td.text)
            count=count+1
            print td.text


print list_symbol
