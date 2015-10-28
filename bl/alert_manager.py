from util import alert_constants, constants
from dao import dbdao
from bl import crossover_manager


    
def fullGapPositive(df):
    diff=df['open']>df['high'].shift(1)
    df= df[diff]
    df['sign']=1
    df['typeid']=alert_constants.Full_Gap_Up
   
    dbdao.savealerts(df)

def fullGapNegative(df):
    diff=df['open']<df['low'].shift(1)
    df= df[diff]
    df['sign']=-1
    df['typeid']=alert_constants.Full_Gap_Down
    
    dbdao.savealerts(df)

def partialGapPositive(df):
    diff=df['open']>df['close'].shift(1)
    df= df[diff]
    df['sign']=1
    df['typeid']=alert_constants.Partial_Gap_up
  
    dbdao.savealerts(df)
    
def partialGapNegative(df):
    diff=df['open']<df['close'].shift(1)
    df= df[diff]
    df['sign']=-1
    df['typeid']=alert_constants.Partial_Gap_Down
  
    dbdao.savealerts(df)
    

def keyReversalPositive(df):
    diff=( (df['open']<df['low'].shift(1)) & (df['close']>df['high'].shift(1)) &(df['volume']>df['sma_volume_6month']) )
    df= df[diff]
    df['sign']=1
    df['typeid']=alert_constants.Positive_Key_Reversal
  
    dbdao.savealerts(df)

def keyReversalNegative(df):
    diff=((df['open']>df['low'].shift(1)) & (df['close']<df['close'].shift(1)) & (df['close']<df['high'].shift(1)) &(df['volume']>df['sma_volume_6month'])) 
    df= df[diff]
    df['sign']=-1
    df['typeid']=alert_constants.Negative_Key_Reversal
   
    dbdao.savealerts(df)    
    
    
def volumePositive(df):
    diff=( (df['volume']>=1.45*df['sma_volume_6month']) )
    df= df[diff]
    df['sign']=1
    df['typeid']=alert_constants.Positive_Volume
   
    dbdao.savealerts(df)

def volumeNegative(df):
    diff=( (df['volume']<0.65*df['sma_volume_6month']) )
    df= df[diff]
    df['sign']=-1
    df['typeid']=alert_constants.Negative_Volume
    
    dbdao.savealerts(df)


    
 
def relative_strength(df_merged):
    
    df_alert= crossover_manager.bullish_co(df_merged,'Relative_strength',alert_constants.Relative_strength,"")
    
    dbdao.savealerts(df_alert)
    #print df_merged
    
#     df_merged["rs"]=df_merged.apply(calculateRelativeStrength,axis=0)
#     print df_merged
    #df.apply(lambda x: x- x.shift(120))
    