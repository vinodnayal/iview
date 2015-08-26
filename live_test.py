import urllib2
from BeautifulSoup import BeautifulSoup
import re
import pandas as pd
from dao import dbdao
from util import loglib
import json

ticker_symbol='MSFT'
url = 'http://finance.google.com/finance/info?q=%s' % ticker_symbol
page = urllib2.urlopen(url,timeout = 10)
html = page.read().replace("//","").strip()
#print html
data  = json.loads(html)
#print data
df=pd.DataFrame(data)
df.set_index('t',inplace=True)
print df
dbdao.save_dataframe(df, "df_live_symbol")