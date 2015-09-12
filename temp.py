import pandas as pd
from dao import dbdao

df=pd.read_csv('data/etf/international.txt',header=None,names=['symbol'])
print df
dbdao.save_dataframe(df, "df_etf")