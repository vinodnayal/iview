import pymongo
from MyConfig import MyConfig as cfg
import pandas


def getsymbol_data( symbol, start_date, end_date):
    
        # connection to server
        con_mongo = pymongo.Connection(cfg.mongodb_host, port=cfg.mongodb_port)
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