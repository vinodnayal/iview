import MySQLdb
import os
from MyConfig import MyConfig as cfg
import MySQLdb.cursors
import pandas.io.sql as psql
import csv
from util import loglib
import datetime
from dateutil.relativedelta import relativedelta
from blaze.tests.test_sql import sql

logger = loglib.getlogger('dbutil_new')



def get_symbols_list():
    
    symbols=[]
    dbcon = MySQLdb.connect(
                            host=cfg.mysqldb_host, user=cfg.mysqldb_user, passwd=cfg.mysqldb_passwd,
                             db=cfg.mysqldb_db)
      
    sql = """
        SELECT DISTINCT symbol FROM list_symbol Where symbol in ("MSFT","AAPL") and  isactive=1 
        """
    cursor = dbcon.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    for row in rows:
        symbols.append(row[0])
    dbcon.close()
    return symbols


def save_dataframe(df,table_name):
        
        dbcon = MySQLdb.connect(
                            host=cfg.mysqldb_host, user=cfg.mysqldb_user, passwd=cfg.mysqldb_passwd,
                             db=cfg.mysqldb_db)
        df.to_sql(con=dbcon, name=table_name, if_exists='replace', flavor='mysql')