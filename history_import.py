from util import loglib
from pandas.io.data import DataReader
import traceback
from dao import dbdao
from dateutil.relativedelta import relativedelta
import datetime
logger = loglib.getlogger('history_import')

def import_data_yahoo_to_files( list_symbols,startdate):       
        #list_error=[]
        logger.info("importing from "+str(startdate))    
        for symbol in  list_symbols:
            try :    
                    print "Historical data for "+symbol            
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
                    dbdao.save_dataframe(prices_df, "df_history_symbol")
                    #prices_df.to_csv(path + "/" + symbol + '.csv')                    
            except Exception as ex:
                logger.error(ex)
                #list_error.append(symbol)
                logger.error(traceback.format_exc())
                
#         f1=open('error_symbols/error.txt', 'a')
#         f1.write(str(list_error))
#         f1.close()
start_date=datetime.datetime.now()
start_date = start_date - relativedelta(years=1)

list_symbol=dbdao.get_symbols_list()

import_data_yahoo_to_files(list_symbol,start_date)