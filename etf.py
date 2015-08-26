import pandas as pd
from os import listdir
from os.path import isfile, join
from dao import dbdao
from pprint import pprint





df= pd.read_csv('data/431conameu.csv',skiprows=2,header=None,names=["name","price_chg","market_Cap","pe","roe","yield","DebttoEquity","PricetoBook","NetProfitMargin","PriceToFreeCashFlow"])

print df[0:2]




dbdao.save_dataframe(df,'df_test')
exit()

path='data/etf/'
onlyfiles = [ f for f in listdir(path) if isfile(join(path,f)) ]

print onlyfiles


def load_data(path,type):
    df= pd.read_csv(path,header=None,names=['symbol'])
    df['type']=type
    df.set_index('symbol',inplace=True)
    return df
    

df_list=[]
for file in onlyfiles:
    full_path= path+file 
    type=file.split('.')[0]
    df_list.append(load_data(full_path,type))
    
df_final=pd.concat(df_list)
print df_final
dbdao.save_dataframe(df_final, "df_etf")
#load_data('data/etf/emerging_mkt.csv','Emerging Mkt')
#load_data('data/etf/commodities.csv','commodities')
    