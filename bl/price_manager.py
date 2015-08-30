from datetime import timedelta

def get_price_date(df,specific_date):
    
    return get_specific_date_value(df, specific_date, 'close')

def get_specific_date_value(df,specific_date,column_name):
    
    try:
        
    
        dfsliced= df[(specific_date-timedelta(days=5)):specific_date]
        #print dfsliced
          
        if len(dfsliced)==0 :
            return df.head(1).iloc[0][column_name]
        else:    
           
            return dfsliced.tail(1).iloc[0][column_name]
    except Exception ,ex:
        raise ex
        

def get_specific_date_data(df,specific_date):
    
    dfsliced= df[(specific_date-timedelta(days=5)):specific_date]
    #print dfsliced
      
    if len(dfsliced)==0 :
        return df.head(1).iloc[0]
    else:    
       
        return dfsliced.tail(1).iloc[0]