from bl import stats_manager 
from dao import dbdao
from util import loglib
import pandas as pd

def correct_name(x):
    
    if('Forward Annual Dividend Yield' in x):
        return 'DividendYield'
    list_exlusion=['Moving Average','52','Annual Dividend','% Held by','Avg Vol','Shares Short (prior','Short %','Ex-Dividend Date']
    for name in list_exlusion:        
        if(name in x):
            return 'drop'
    
    x=x.strip().replace(' ','')
    x=x.strip().replace('/','')
    return x.split('(')[0].split(':')[0].strip()



logger = loglib.getlogger('stats')
import sys
print sys.argv
start,end=sys.argv[1],sys.argv[2]

df_all= pd.DataFrame()
#list_symbol=dbdao.get_symbols_list_limit(start,end)
list_symbol=dbdao.get_missing_stats_symbol(start,end)


if(start=='0'):
        dbdao.execute_query(["delete from df_stats"])
        
print list_symbol
logger.info(list_symbol)

for symbol in list_symbol:
    try:
        systats_data = stats_manager.yf_get_key_stat(symbol)
        logger.info('calculating for symbol '+symbol)
        systats_data.append(['symbol',symbol])
        df= pd.DataFrame(systats_data)
        if(df.shape[0] >10):    
            df = df.rename(columns={0: 'name'})
            df['name']= df['name'].apply(correct_name)
            df= df[df['name']!='drop']
            df= df.set_index('name').transpose()
            print df
            df_all=df_all.append(df)
    except Exception,ex:
        logger.error(ex)
print df_all
df_all.to_csv('data/df.csv');


dbdao.save_dataframe(df_all,'df_stats')

# dbdao.execute_query(["Delete from fin_stats_symbol"])
# 
# for symbol in list_symbol:
#     list_function=[stats_manager.get_IncomeStatement(symbol),stats_manager.get_BalanceSheet(symbol),stats_manager.get_CashFlow(symbol)]
#     for function_name in list_function:
#         function_name 
