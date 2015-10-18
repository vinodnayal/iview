import pymongo
import MySQLdb
from MyConfig import MyConfig as cfg
import pandas
import pandas as pd

def getsymbol_data( symbol, start_date, end_date):
    
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
            
        
            list_drop_cloumns = [ '_id', 'actualclose','volume','symbol']
            prices_df = prices_df.drop(list_drop_cloumns, 1)
            
            
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
        
def getsymbol_data_temp(symbol, start_date_time, end_date_time):
    
    symbols=[]
    dbcon = MySQLdb.connect(
                            host=cfg.mysqldb_host, user=cfg.mysqldb_user, passwd=cfg.mysqldb_passwd,
                             db=cfg.mysqldb_db)
      
    sql = """
        select date,close,open,low,high from history_symbol where symbol ='%s'
        """%symbol
        
    df=pd.read_sql(sql, con=dbcon)    
    df=df.sort("date")
    df.set_index('date',inplace=True)
    
    dbcon.close()
    return df