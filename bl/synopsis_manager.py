
import util

ratingStrength={0:"Very Weak",1:"",2:""}
def calculateSynopsis(row):
    rating=1
    is_macd_crossover_signal=True
    is_macd_crossover_center=False
    fifty_two_week_high=True
    macd=1.0
    rsi=1
    symbol="MSFT"
    rating_text="weak"
    up_or_down="up"
    symbol_twelve_month_return="10 %"
    spy_twelve_month_return=" 5 %"
    positive_key_reversal=True
    negative_key_reversal=True
    
    
    current_situation="""%s is currently rated a %d out of 10 on the technical rating score, which technically 
    is the %s reading. For the last 12 months %s is %s 
     %s compared to the S&P 500' %s."""%(symbol, rating  ,rating_text,symbol,up_or_down ,symbol_twelve_month_return,spy_twelve_month_return)
    if(rating ==10  ):     
        text1=""" If you are long : Currently %s is technically very strong and is not showing any evidence of the overall trend weakening"""%symbol
        
        text2="""If you want to buy:If you are looking to initiate a position in %s, the stock is still 
        showing longer term strength.  However, make sure the short term trend is very bullish coupled
         with increasing momentum measured by the MACD and RSI before going long. """%symbol
    
    elif(rating ==9  ):
        text1="""If you are long:Currently, %s is technically very strong and is not showing evidence of the overall 
        trend weakening. """%symbol
        text2="""If you want to buy:If you are looking to initiate a position in %s, the stock is still showing longer term strength. However, 
        make sure the short term trend is very bullish coupled with increasing momentum measured by the MACD and RSI 
        before going long."""%symbol
         
    elif(rating ==8  ):
        text1="""If you are long:Currently, %s is technically strong and the price action is not 
         signaling any negative events reflective in the stock"""%symbol
        text2="""If you want to buy:If you are looking to initiate a position in %s, the stock is still showing longer term strength. 
         However, make sure the short term trend is very bullish coupled with increasing momentum measured by the MACD and 
         RSI before going long. """%symbol
    
    elif(rating ==7 ):
        text1="""If you are long:Currently, %s is technically strong"""%symbol
        text2="""If you want to buy:If you are looking to initiate a position in %s, the stock is still showing longer term strength.  
        However, make sure the
         short term trend is very bullish coupled with increasing momentum 
         measured by the MACD and RSI before going long.  """ %(symbol,symbol)
    elif(rating ==6 ):
        text1="""If you are long:Currently, %s is not showing any evidence of the overall trend weakening or significantly 
        increasing at the current level."""%symbol
        text2="""If you want to buy:If you are looking to initiate a position in %s, look for an increase in the trend score couple 
        with increasing momentum measured by the MACD and RSI before going long. """ %symbol
    elif(rating ==5 ):
        text1="""If you are long:Currently, %s is not showing any evidence of the overall 
        trend weakening or significantly increasing at the current level. """%symbol
        text2="""If you want to buy:If you are looking to initiate a position in %s, look for an 
        increase in the trend score couple with increasing momentum measured by the MACD and RSI before going long. """ %symbol
         
    elif(rating ==4 ):
        text1="""If you are long:Currently, %s is basically neutral
         and in a holding pattern and not showing evidence of any significant directional trend moves"""%symbol
        text2="""If you want to buy:If you are looking to initiate a position in %s, the stock is basically neutral. 
         Wait for confirmation of stronger price action measured by a increase in the trend score, coupled with increasing 
         momentum measured by the MACD and RSI before going long  """ %symbol
    elif(rating ==3 ):
        text1="""If you are long:Currently, %s is basically neutral and in a holding 
        pattern and not showing evidence of any significant directional trend moves. """%symbol
        text2="""If you want to buy:If you are looking to initiate a position in %s, the stock is basically neutral. 
         Wait for confirmation of stronger price action  measured by a increase in the trend score,
          coupled with increasing momentum measured by the MACD and RSI before going long. """%symbol 
    elif(rating ==2 ):
        text1=""""""
        text2="""%s price action at the current level is not showing a high probability of higher prices. 
         Wait for confirmation of a greater trend score to entry to the long  side.  Additionally,  watch for increasing momentum 
          measured by the MACD before going long for additional confirmation.""" %symbol
             
    elif(rating ==1 ):
        text1=""""""
        text2="""To mitigate downside risk, %s trend rating is not showing evidence of higher price appreciation at current levels. 
          Wait for confirmation of price stabilization accompanied by a steady increase in the technical trend  score.  
          Remember, look for the short and medium term trends to improve to a very bullish stance coupled with increasing
           momentum measured by the MACD before going long"""   %symbol

    elif(rating ==0 ):
        text1=""""""
        text2="""To mitigate downside risk, %s trend rating is not showing evidence of higher price appreciation at current levels.   
        Wait for confirmation of price stabilization accompanied by a steady increase in the technical trend  score.  
        Remember, look for the short and medium term trends to improve to a very bullish stance coupled with increasing 
        momentum measured by the MACD before going long. """ %symbol
        
    # if there is alert calculate synopsis for it  
     
    if(positive_key_reversal and ( rating ==0 or rating ==1)):
        text1=""""""
        text2="""If you are long: Alert: Currently, %s is technically very weak, however,  %s just had a positive Key Reversal and might 
        experience short term upward bounce.  This typically occurs when the stocks price achieves its lowest price over 
        the last 200 days and Todays open is lower then the previous low.  This is coupled with a closing price higher  
        than the previous days close and the high.  Lastly, a key reversal is accompanied with higher volume. """ %(symbol,symbol)
           
    if(rating >=7 and rsi == util.constants.RSI_ExtremelyOverbought):
        text1=""" If you are long:Although %s technically is very strong, it is showing signs of being extremely overbought 
        according to the RSI, which has a reading of (SHOW RSI).  
        Reducing partial exposure maybe warranted to lock in potential profits.  """%symbol
        
        text2=""" If you want to buy:If you are looking to initiate a position in %s, the stock is showing strong relative strength, 
        however, it is overbought.   Look for a pullback to longer term support as a potential opportunity.  
        Please refer to daily support and resistance level  on the bottom right of this page. """%symbol
    if(rating >=7 and rsi == util.constants.RSI_Overbought):
        text1=""" If you are long:Although %s technically is very strong, the stock is  overbought according to the RSI,
         which has a reading of (SHOW RSI).  Reducing partial exposure maybe warranted to lock in potential profits.   """%symbol
        
        text2=""" If you are looking to initiate a position in %s, the stock is still showing longer term strength, however,
         it is at overbought level. 
          Make sure the momentum (MACD and or RSI) is still increasing before establishing a long position."""%symbol
    
    if(rating >=7 and is_macd_crossover_center):
        text1=""" """
        
        text2="""If you are long:Alert: %s technically is very strong, additionally, the stock is showing signs 
        of additional momentum to the upside as the MACD crossed above the zero line on (Day Date Year).  
        """%symbol
        
    if(rating >=7 and fifty_two_week_high):
        text1="""If you are long: Alert:  %s hit a new 52 week high on Day Date Year.  
        Currently, %s is technically very strong and is not showing any evidence of the overall trend weakening . """%(symbol,symbol)
        
        text2="""If you want to buy:If you are looking to initiate a position in %s, the stock is still
         showing longer term strength.  However, make sure the short term trend is very bullish coupled with 
         increasing momentum measured by the MACD before going long.  
        """%symbol
    if(rating >=5 and negative_key_reversal):
        text1="""If you are long: Alert:  %s hit a new 52 week high on Day Date Year.  
        Currently, %s is technically very strong and is not showing any evidence of the overall trend weakening . """%(symbol,symbol)
        
        text2="""If you are long:Alert: Currently, %s is technically very strong, however, 
         XYZ just had a negative Key Reversal and might experience short term downside pressure.  
         This typically occurs when the stocks price achieves its highs price over the last 200 days
          and Today's open is higher then the previous high.  This is coupled with a closing price lower 
          than the previous days close and the low.  Lastly, a key reversal is accompanied with higher volume. 
 
        """%symbol
        
        
    net_text=current_situation +"<br/>" +text1+"<br/>"+text2
    return net_text
    
    