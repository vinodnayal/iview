

def Short_term(latest_row):

    short_sum=0
    
    if (latest_row['sma3'] > latest_row['sma9']):
        short_sum=short_sum+1
    else:    
        short_sum=short_sum  
         
    if (latest_row['sma5']) > (latest_row['sma13']):
        short_sum=short_sum+1
    else:    
        short_sum=short_sum
        
    if (latest_row['sma5']) > (latest_row['sma20']):
        short_sum=short_sum+1
    else:    
        short_sum=short_sum  
    
    if (latest_row['rsi']) > 50:
        short_sum=short_sum+1
    else:    
        short_sum=short_sum  
    
    if (latest_row['rsi']) > 70:
        short_sum=short_sum+1
    else:    
        short_sum=short_sum
    
    if (latest_row['rsi']) < 30:
        short_sum=short_sum+1
    else:    
        short_sum=short_sum
    
    return short_sum      
    

def Intermediate_term(latest_row):

    inter_sum=0
    
    if (latest_row['sma25'] > latest_row['sma90']):
        inter_sum=inter_sum+1
    else:    
        inter_sum=inter_sum
          
    if (latest_row['sma13']) > (latest_row['sma50']):
        inter_sum=inter_sum+1
    else:    
        inter_sum=inter_sum

    if (latest_row['sma25']) < (latest_row['sma90']):
        inter_sum=inter_sum+1
    else:    
        inter_sum=inter_sum  
    
    if (latest_row['sma50']) < (latest_row['sma13']):
        inter_sum=inter_sum+1
    else:    
        inter_sum=inter_sum  
    
    return inter_sum       
    
   
def Long_term(latest_row):

    long_sum=0
    
    if (latest_row['sma36'] > latest_row['sma150']):
        long_sum=long_sum+1
    else:    
        long_sum=long_sum
     
    if (latest_row['sma50']) > (latest_row['sma200']):
        long_sum=long_sum+1
    else:    
        long_sum=long_sum

    return long_sum        
    

