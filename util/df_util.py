import pandas as pd
import os
def create_dataframe(path_dir,index,type=None):
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
    df_net.set_index(index,inplace=True)
    return df_net