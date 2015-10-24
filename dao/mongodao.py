import pymongo
import MySQLdb
from MyConfig import MyConfig as cfg
import pandas
import pandas as pd

def getsymbol_data( symbol, start_date, end_date):
    
    df= getSymbolData(symbol, start_date, end_date)
    list_drop_cloumns = [ '_id', 'actualclose','symbol']
    df = df.drop(list_drop_cloumns, 1)
    return df
  
def getSymbolDataWithSymbol( symbol, start_date, end_date):
    
    df= getSymbolData(symbol, start_date, end_date)
    list_drop_cloumns = [ '_id', 'actualclose']
    df = df.drop(list_drop_cloumns, 1)
    return df  

def getSymbolData( symbol, start_date, end_date):
    
        # connection to server
        con_mongo = pymongo.MongoClient(cfg.mongodb_host, port=cfg.mongodb_port)
        #database is chartlab
        db_chartlab = con_mongo.chartlab
        # prices_data = db_chartlab.symbolshistorical.find({"symbol":symbol})
        
        # table(collection) is symbolshistorical
        prices_data = db_chartlab.symbolshistorical.find({"$and" : [{'symbol':symbol},
                                                              {"date": {"$gt": start_date}},
                                                               {"date": {"$lt": end_date}}]}).sort("date", 1)
         
        prices_df = pandas.DataFrame(list(prices_data))
        if(not prices_df.empty):
            
        
            
            
            
            con_mongo.close()
            if(len(prices_df)) > 0:
                
                prices_df = prices_df.set_index('date')
            
            
        return prices_df
    

def remove_symbol(symbol,coll_name):
        # symbol_list = ["CAH", "CELG", "CMG", "COP", "CTSH", "EOG", "HES", "MCK", "MHFI"]
       
        con_mongo = pymongo.MongoClient(cfg.mongodb_host, port=cfg.mongodb_port)
        db_chartlab = con_mongo.chartlab
        db_chartlab.symbolshistorical.remove({"symbol":symbol})
        con_mongo.close()
        
