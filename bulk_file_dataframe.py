import os
import pandas as pd
from dao import dbdao
from util import df_util

def saveindb(path_dir,type=None):
    df_net=None
    for root, dirs, files in os.walk(path_dir):
        
        for file in files:
            if file.endswith(".csv"):
                 print(os.path.join(root, file))
                 df =pd.read_csv(os.path.join(root, file),sep="^")
                 if(df_net is None ):
                     df_net=df
                 else:
                    df_net=df_net.append(df)                 
    if(type is not None):
        df_net['type']=type
    df_net.set_index("Symbol",inplace=True)
    dbdao.save_dataframe(df_net, "df_stats_quarter")




#dbdao.execute_query(["delete from df_stats_quarter"])
df=df_util.create_dataframe("data\\stats\\balance_sheet","Symbol", type="Balance Sheet")
dbdao.save_dataframe(df, "df_stats_quarter")
df=df_util.create_dataframe("data\\stats\\income_statement","Symbol", type="Income Statement")
dbdao.save_dataframe(df, "df_stats_quarter")
df=df_util.create_dataframe("data\\stats\\cash_flow","Symbol", type="Cash Flow")
dbdao.save_dataframe(df, "df_stats_quarter")



