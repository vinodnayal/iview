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
    

def bullish_co(df,column1):

    previous = df[column1].shift(1)
   
    crossing = ((df[column1] >=0) & (previous <0))
                
    crossing_dates = df.loc[crossing]
    print(crossing_dates)
    

def bearish_co(df,column1):

    previous = df[column1].shift(1)
   
    crossing =  ((df[column1]<= 0) & (previous >0))
    crossing_dates = df.loc[crossing]
    print(crossing_dates)
    
    