from dao2 import dbdao
from util import loglib, datetimeutil, constants
from bl import historical_dates_manager
import csv


logger = loglib.getlogger('historical_dates_manager')

def calculate_history_dates():
    #mysqldao=dbutil.mysqldb()
    #print technicals.gethistory_dates() 
    header=("DateType,Date")
    hist_dates=historical_dates_manager.gethistory_dates()  
    filename='data/historical_date/hist_dates'
    f1=open(filename, 'wb')
    f1.write(header)
    f1.write('\n')
    writer = csv.writer(f1)
    for key, value in hist_dates.items():
        writer.writerow([key, value])
     
    f1.close()
    
    delete_sql="delete from historicaldates"
    insert_sql="""
                LOAD DATA LOCAL INFILE '%s'
                INTO TABLE historicaldates
                FIELDS TERMINATED BY ','
                LINES TERMINATED BY "\n" 
                IGNORE 1 LINES                
                (@DateType,@Date)                
                SET DateType=@DateType,Date=@Date
              """%(filename)
    logger.info("Saving Historical Dates to database") 
    dbdao.execute_query([delete_sql,insert_sql])
    logger.info("Saved Historical Dates to database")
    
    
calculate_history_dates()