from pandas.io.data import DataReader
import pymongo

import shutil
import pandas as pd
import datetime


from MyConfig import MyConfig as cfg

import traceback



import os
import MySQLdb


from util import loglib
from dao import dbdao, mongodao
logger = loglib.getlogger('dataimport')

BS_START_DATE=datetime.datetime(1993, 01, 01)
NONBS_START_DATE=datetime.datetime(2010, 01, 01)


#path = 'historical_data/' 
    

        
def import_data_yahoo_to_files( list_symbols,path,startdate):       
        list_error=[]
        logger.info("importing from "+str(startdate))    
        for symbol in  list_symbols:
            try :                
                    prices_df = DataReader(symbol, "yahoo", startdate)                
                    count_newdata = len(prices_df)
                    print  symbol , " ", count_newdata     
                    if(count_newdata <=0):
                        raise Exception("NO DATA for Dates for %s"%symbol)           
                    prices_df = prices_df.rename(columns={'Date': 'date', 'Open': 'open', 'High': 'high',
                                                   'Low': 'low', 'Close': 'actualclose', 'Adj Close': 'close',
                                                   'Volume': 'volume', 'Symbol': 'symbol'})
                    prices_df['symbol'] = symbol             
                    prices_df['symbol'] = prices_df.apply(lambda x: x['symbol'].replace('\r','').upper(), axis=1 )    
                    prices_df.to_csv(path + "/" + symbol + '.csv')                    
            except Exception as ex:
                logger.error(ex)
                list_error.append(symbol)
                logger.error(traceback.format_exc())
                
       

def import_data_from_files_todb(path):        
        
        abspath = os.path.abspath(path) + "\\"
        logger.info(abspath)
        list_files = os.listdir(path)
        dbcon = MySQLdb.connect(
                            host=cfg.mysqldb_host, user=cfg.mysqldb_user, passwd=cfg.mysqldb_passwd,
                             db=cfg.mysqldb_db)
        for filename in list_files:
            
            symbol = filename.strip('.csv')
            logger.info("for symbol"+symbol)
            filename = abspath + filename
            filename = filename.replace("\\", "//")
            
            #del_sql = "delete from symbolshistorical where symbol='%s'" % (symbol)
            sql = """LOAD DATA LOCAL INFILE  '%s' INTO TABLE history_symbol 
                    FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 LINES
                    (@date,@open,@high,@low,@actualclose,@volume,@close,@symbol) 
                    set date=@date,open=@open,high=@high,low=@low,actualclose=@actualclose,volume=@volume,close=@close,
                    symbol=replace(@symbol,'\r','')""" % (filename)          
            
            #logger.info( sql)
            cursor = dbcon.cursor()
            #cursor.execute(del_sql)            
            cursor.execute(sql)
            dbcon.commit()
        dbcon.close()


def import_data_from_files_tomongo(path,shoulddelete): 
        con_mongo = pymongo.MongoClient(cfg.mongodb_host, port=cfg.mongodb_port)
        db_chartlab = con_mongo.chartlab 
         
        abspath = os.path.abspath(path) + "\\"
        logger.info(abspath)
        list_files = os.listdir(path)
        
        count=0
        for filename in list_files:
            try:
                symbol = filename.strip('.csv')
                count=count+1
                logger.info("for symbol"+symbol+": "+str(count))
                filename = abspath + filename
                filename = filename.replace("\\", "//") 
                prices_df=pd.read_csv(filename)
                prices_df = prices_df.rename(columns={'Date': 'date', 'Open': 'open', 'High': 'high',
                                                       'Low': 'low', 'Close': 'actualclose', 'Adj Close': 'close',
                                                       'Volume': 'volume', 'Symbol': 'symbol'})
                    
                
                #print prices_df[0:5]    
                if(len(prices_df)>0):
                    if(shoulddelete):
                        
                        db_chartlab.symbolshistorical.remove({"symbol":symbol})            
                    prices_df['date'] = prices_df.apply(lambda x: getdatetime(x['date']), axis=1 )       
                    prices_df['symbol'] = prices_df.apply(lambda x: x['symbol'].replace('\r','').upper(), axis=1 )
                    for a in prices_df.iterrows():        
                                tempdict = a[1].to_dict()
                                #print tempdict                                                 
                                db_chartlab[col_name].insert(tempdict) 
            except Exception ,ex:
                logger.error(ex)
                logger.error( traceback.format_exc())                     
        
        con_mongo.close()
          
                


def getdatetime(date_in):
 
    date=datetime.datetime.strptime(date_in, '%Y-%m-%d')
 
    return date
   



	
    


def importdata(list_symbols):
    try:
        
        foldername= datetime.datetime.now().strftime("%Y-%m-%d")
#         print foldername
#         bs_list_symbols=dbdao.get_spy_symbols_list()
        path="data/symbol_import/"+str(foldername)
#         createpath(path)
#         
#         
#      
#         normal_symbols=[]
#         snp_symbols=[]
#         for symbol in list_symbols:
#             if(symbol in bs_list_symbols):
#                 snp_symbols.append(symbol)
#             else:
#                 normal_symbols.append(symbol)
#                     
#         if(len(snp_symbols)>0):
#             import_data_yahoo_to_files(snp_symbols,path,BS_START_DATE)
#         if(len(normal_symbols)>0):
#             import_data_yahoo_to_files(normal_symbols,path,NONBS_START_DATE)
        
        for symbol in list_symbols:            
            dbdao.remove_symbol(symbol)
            mongodao.remove_symbol(symbol)
            
        import_data_from_files_todb(path)
        import_data_from_files_tomongo(path,False)
        
    except Exception ,ex:
        logger.error(ex)
        logger.error( traceback.format_exc()) 	
	

def createpath(path):
    if(os.path.exists(path)):
            shutil.rmtree(path)
                   
    os.makedirs(path)

   
