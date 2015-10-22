import pandas as pd




    
def give_positive_co_dates(df,column1,column2):

    previous_col1 = df[column1].shift(1)
    previous_col2 = df[column2].shift(1)
    crossing = ((df[column1] >= df[column2]) & (previous_col1 <= previous_col2))
    crossing_dates = df.loc[crossing]
    crossing_dates['sign']=1
    print(crossing_dates)
    
def give_negative_co_dates(df,column1,column2):

    previous_col1 = df[column1].shift(1)
    previous_col2 = df[column2].shift(1)
    crossing = ((df[column1] <= df[column2]) & (previous_col1 >= previous_col2))
            
    crossing_dates = df.loc[crossing]
    print(crossing_dates)
    

def bullish_above(df,column1):

    
   
    crossing = ((df[column1] >=0) )
                
    crossing_dates = df.loc[crossing]
    print(crossing_dates)

def bearish_below(df,column1):

    
   
    crossing = ((df[column1] >=0) )
                
    crossing_dates = df.loc[crossing]
    print(crossing_dates)
    

def macd_crossovers(df):  
    df_bull_signal= bullish_co(df, 'macdhist',1)
    
    df_bear_signal=bearish_co(df, 'macdhist',2)
    df_bull_center= bullish_co(df, 'macd',3)
    df_bear_center=bearish_co(df, 'macd',4)
    df_merged=pd.concat([df_bull_signal,df_bear_signal,df_bull_center,df_bear_center],axis=0)  
    return df_merged 
        
def bullish_co(df,column1,typeid):

    previous = df[column1].shift(1)
   
    crossing = ((df[column1] >=0) & (previous <0))
     
                
    crossing_dates = df.loc[crossing]
    crossing_dates['sign']=1
    crossing_dates['typeid']=typeid
    return crossing_dates
    

def bearish_co(df,column1,typeid):

    previous = df[column1].shift(1)
   
    crossing =  ((df[column1]<= 0) & (previous >0))
    crossing_dates = df.loc[crossing]
    crossing_dates['sign']=-1
    crossing_dates['typeid']=typeid
    return crossing_dates
    
    