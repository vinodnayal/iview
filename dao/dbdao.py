import MySQLdb
import os
import pandas as pd
from MyConfig import MyConfig as cfg
import MySQLdb.cursors
import pandas.io.sql as psql
import csv
from util import loglib
import datetime
from dateutil.relativedelta import relativedelta
from blaze.tests.test_sql import sql
from mock import inplace

logger = loglib.getlogger('dbutil_new')

def execute_query(list_sql):
        
        dbcon = MySQLdb.connect(
                            host=cfg.mysqldb_host, user=cfg.mysqldb_user, passwd=cfg.mysqldb_passwd,
                             db=cfg.mysqldb_db)
        
    
        for sql in list_sql:
        
            logger.info('executing query '+sql)
            cursor=dbcon.cursor()
            #print sql
            cursor.execute(sql)

            print cursor.rowcount
            

        dbcon.commit()
        
        
        dbcon.close()                    





def get_data_db_frame(sql):
    dbcon = MySQLdb.connect(
                            host=cfg.mysqldb_host, user=cfg.mysqldb_user, passwd=cfg.mysqldb_passwd,
                             db=cfg.mysqldb_db)
        
    df=pd.read_sql(sql, con=dbcon)    
    dbcon.close()
    return df


def get_symbols_list_limit(start,end):
    
    symbols=[]
    dbcon = MySQLdb.connect(
                            host=cfg.mysqldb_host, user=cfg.mysqldb_user, passwd=cfg.mysqldb_passwd,
                             db=cfg.mysqldb_db)
      
    sql = """
        SELECT DISTINCT symbol FROM list_symbol  limit %s,%s
        """%(start,end)
    print sql
   
    cursor = dbcon.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    for row in rows:
        symbols.append(row[0])
    dbcon.close()
    return symbols
def get_missing_stats_symbol(start,end):
    
    symbols=[]
    dbcon = MySQLdb.connect(
                            host=cfg.mysqldb_host, user=cfg.mysqldb_user, passwd=cfg.mysqldb_passwd,
                             db=cfg.mysqldb_db)
      
    sql = """
                    select distinct t1.symbol from list_symbol  t1 
            left join stats t2 
            on t1.symbol=t2.symbol
            where t2.symbol is null limit %s,%s
        """%(start,end)
    print sql
   
    cursor = dbcon.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    for row in rows:
        symbols.append(row[0])
    dbcon.close()
    return symbols


def get_symbols_list():
    
    symbols=[]
    dbcon = MySQLdb.connect(
                            host=cfg.mysqldb_host, user=cfg.mysqldb_user, passwd=cfg.mysqldb_passwd,
                             db=cfg.mysqldb_db)
      
    sql = """
        select distinct symbol from list_symbol
        """


    cursor = dbcon.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    for row in rows:
        symbols.append(row[0])
    dbcon.close()
    return symbols

def get_symbols_list_missing():
    
    symbols=[]
    dbcon = MySQLdb.connect(
                            host=cfg.mysqldb_host, user=cfg.mysqldb_user, passwd=cfg.mysqldb_passwd,
                             db=cfg.mysqldb_db)
      
    sql = """
        select t1.symbol from spy_symbol t1
            left join list_symbol t2
            on t1.symbol=t2.symbol
            where t2.symbol is null    
        """


    cursor = dbcon.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    for row in rows:
        symbols.append(row[0])
    dbcon.close()
    return symbols



def get_indices_symbols_list():
    
    symbols=[]
    dbcon = MySQLdb.connect(
                            host=cfg.mysqldb_host, user=cfg.mysqldb_user, passwd=cfg.mysqldb_passwd,
                             db=cfg.mysqldb_db)
      
    sql = """
        select distinct googsymbol from indices_symbol     
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
        df.to_sql(con=dbcon, name=table_name, if_exists='append', flavor='mysql')
        dbcon.close()
        
        

def get_historical_dates():
        dates = []
        dates_dict={}
        dbcon = MySQLdb.connect(
                            host=cfg.mysqldb_host, user=cfg.mysqldb_user, passwd=cfg.mysqldb_passwd,
                             db=cfg.mysqldb_db)
        sql = """
        select datetype,date from historicaldates
        """
        
        cursor=dbcon.cursor()
        cursor.execute(sql)
        rows=cursor.fetchall()
        for row in rows:
            dates.append(row)
            dates_dict.update({row[0]:row[1]})
        dbcon.close()
        return dates_dict
    