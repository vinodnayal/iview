from util import  constants
import pandas as pd
def calculate_rsi_values(p):
    
            if (p < 20 ):
            
                r = constants.RSI_ExtremelyOversold
            
            elif (p >= 20 and p <= 30):
            
                r = constants.RSI_Oversold
            
            elif (p > 30 and p <= 45):
            
                r = constants.RSI_ApproachingOversold
            
            elif (p > 45 and p <= 55):
            
                r = constants.RSI_Neutral
            
            elif (p > 55 and p <= 70):
            
                r = constants.RSI_ApproachingOverbought           
           
            elif (p > 70 and p <= 80):
            
                r = constants.RSI_Overbought
            
            elif (p > 80):
            
                r = constants.RSI_ExtremelyOverbought
            else :
                r=None
                
            return r

def obos_alerts(df):

    
    
    df['rsi_value'] = df['rsi'].apply(calculate_rsi_values )
   
    
    
   
     
   
    df_aos = df.loc[df['rsi_value'] ==constants.RSI_ApproachingOversold]
  
    df_aos['sign']=1
    df_aos['typeid']=5
    
    
    df_os = df.loc[(df['rsi_value'] ==constants.RSI_Oversold)]
    df_os['sign']=1
    df_os['typeid']=6
    
    
    df_aob= df.loc[(df['rsi_value'] ==constants.RSI_ApproachingOverbought)]
    df_aob['sign']=-1
    df_aob['typeid']=7
    
    
    df_ob = df.loc[(df['rsi_value'] ==constants.RSI_Overbought)]
    df_ob['sign']=-1
    df_ob['typeid']=8
    
    
    
    df_merged = pd.concat([df_aob,df_aos,df_os,df_ob],axis=0)
    
    df_merged=df_merged.drop(['close','rsi','rsi_value'],1)
    
    return df_merged