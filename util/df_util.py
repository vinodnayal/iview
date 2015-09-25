import pandas as pd
import os
from dao import dbdao
def create_dataframe(path_dir,index,type,table_name):
    for root, dirs, files in os.walk(path_dir):
        for file in files:
            if file.endswith(".csv"):
                 try:
                     print(os.path.join(root, file))
                     df =pd.read_csv(os.path.join(root, file),sep="^")
                     df['type']=type
                     df.set_index(index,inplace=True)
                     dbdao.save_dataframe(df, table_name)
                 except Exception,ex:
                     print ex
                
