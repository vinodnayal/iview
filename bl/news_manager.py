from util import loglib
from dao2 import dbdao
import os
import urllib
import urllib2
from xml.dom import minidom
from BeautifulSoup import BeautifulSoup
import csv
from IPython.core.page import page
# from xml.etree import ElementTree as etree
import feedparser
import lxml.html, lxml.etree

            
            
def save_NEWS(filepath): #### Main News Program ######
    
    logger = loglib.getlogger('news_util')

    url_dict={"Market Realist":['http://marketrealist.com/feed/'],
               "ValueWalk":['http://feeds.feedburner.com/VWTwitterFeed'],
               "ECONOMIST":['http://www.economist.com/sections/business-finance/rss.xml'],
               "YahooFinance":['http://finance.yahoo.com/news/rss'],
               "CNBC":["http://www.cnbc.com/id/15839135/device/rss/rss.html"],
               "BusinessInsider":["http://feeds.feedburner.com/businessinsider"],
               "MarketWatch":["http://feeds.marketwatch.com/marketwatch/realtimeheadlines"],
               "Reuters":["http://feeds.reuters.com/news/usmarkets"],
               "Bloomberg View":["http://www.bloombergview.com/rss"],
               "ZeroHedge":["http://feeds.feedburner.com/zerohedge/feed"],
               "BIDNESS ETC":["http://www.bidnessetc.com/businessnewsfeed/"],
               "Benzinga":["http://feeds.benzinga.com/benzinga/analyst-ratings/price-target"
                           ,"http://feeds.benzinga.com/benzinga/analyst-ratings/downgrades","http://feeds.benzinga.com/benzinga/analyst-ratings/upgrades"
                           
                           ]}

    seperator="LINE_SEPERATOR"     
    f1=open(filepath,'w')
    header="Source"+seperator+"Title"+seperator+"Description"+seperator+"Link"+seperator+"pubDate"
    f1.write(header)
    f1.write('\n')        
   
    for url_name,list_url in url_dict.iteritems():
        for url in list_url: 
            feed = feedparser.parse(url)        
            try:
                logger.info("Getting news for" + url_name)
                 
                for entry in feed["entries"]:
                    list_entries=[]
                    list_entries.append(url_name)
                    list_entries.append(entry.title)
                    list_entries.append(entry.summary)
                    list_entries.append(entry.link)
                    list_entries.append(entry.published)           
                    content=seperator.join(list_entries)            
                    #print content
                    f1.write(content.encode('ascii', 'ignore').strip().replace("\n",""))
                    f1.write("\n")
                                
            except Exception ,ex:
                    logger.error(ex)        
            
    f1.close()
    
    sql1="delete from news_details"   
    sql2="""LOAD DATA LOCAL INFILE '%s'
        INTO TABLE news_details 
        FIELDS TERMINATED BY '%s' 
        LINES TERMINATED BY "\n"
        IGNORE 1 LINES
        (@col1,@col2,@col3,@col4,@col5) set source=@col1,title=@col2,description=@col3,link=@col4,pubDate=@col5
        ;"""%(filepath,seperator)
    dbdao.execute_query([sql1,sql2])       
                
