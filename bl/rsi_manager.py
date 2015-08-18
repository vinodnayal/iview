from util import  constants
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
                
            return r
