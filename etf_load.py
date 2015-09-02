import pandas as pd
from dao2 import dbdao

df=pd.read_csv('data/etf/assets.csv')

list_assets=df.columns.values


df_net=pd.DataFrame()
frames=[]

for asset in list_assets:   
    df_temp=pd.DataFrame() 
    df_temp['symbol']=df[asset]
    df_temp['asset']=asset
    df_temp=df_temp.dropna()
    df_temp=df_temp.set_index('symbol')
    
    frames.append(df_temp)

df_net=pd.concat(frames)
print df_net


dbdao.save_dataframe(df_net, "df_etf_load")