import datetime
import datetime as dt
from dateutil.relativedelta import relativedelta
#from utils import fin

from util import loglib, datetimeutil, constants
from datetime import timedelta
from dao import mongodao
logger = loglib.getlogger('technicals')



def gethistory_dates():
    end_date = dt.datetime.now()
    start_date = end_date + relativedelta(years=-2)
    # df1 = mongodao.get_symbollist_data(list_symbols, start_date, end_date)
    curdate = dt.datetime.now().date()
    month = curdate.month
    
    monthstartdate = dt.date(curdate.year, curdate.month, 1)
    yearstartdate = dt.date(curdate.year, 1, 1)
    if (month > 3):
                    
                        if (month > 3 and month <= 6):
                        
                            quatermonth = 4;
                        
                        elif (month > 6 and month <= 9):
                        
                            quatermonth = 7;
                        
                        elif (month > 9 and month <= 12):
                        
                            quatermonth = 10;
                        
                    
    else:
                    
                        quatermonth = 1;
    
    weekstart = curdate - timedelta(days=(curdate.weekday() + 1) % 7)
    quarterstartdate = dt.date(curdate.year, quatermonth, 1) - timedelta(days=1)                
     
    #mongodbdao = mongoutil.
    prices_mkt = mongodao.getsymbol_data(constants.MKT_SYMBOL, start_date, end_date)
   
    oneyearbeforedate=curdate - relativedelta(years=1)
    oneMonth=curdate - relativedelta(months=1)
    
    oneyearbeforedate = datetimeutil.getdate(getspecificdate(oneyearbeforedate, prices_mkt)) 
    oneMonth = datetimeutil.getdate(getspecificdate(oneMonth, prices_mkt))
    yesterday = datetimeutil.getdate(getspecificdate(curdate - timedelta(days=1), prices_mkt))
    
    day2 = datetimeutil.getdate(getspecificdate(curdate - timedelta(days=2), prices_mkt))
    day3 = datetimeutil.getdate(getspecificdate(curdate - timedelta(days=3), prices_mkt))
    day5 = datetimeutil.getdate(getspecificdate(curdate - timedelta(days=5), prices_mkt))
    
    weekdstart = datetimeutil.getdate(getspecificdate(weekstart, prices_mkt))
    monthstart = datetimeutil.getdate(getspecificdate(monthstartdate, prices_mkt))
    quaterstart = datetimeutil.getdate(getspecificdate(quarterstartdate, prices_mkt))
    yearstart = datetimeutil.getdate(getspecificdate(yearstartdate, prices_mkt))
    
    return {"current":curdate, "PreviousDay":yesterday, "2days":day2, "3days":day3, "5days":day5, 
            "Weekly":weekdstart, "Monthly":monthstart, "Quaterly":quaterstart, 
            "Yearly":yearstart, "oneyearbeforedate":oneyearbeforedate,"oneMonth":oneMonth}



def getspecificdate(date,df1):
    
    date_str=datetimeutil.getdatestr(date)
    five_days_before_str=datetimeutil.getdatestr(date-timedelta(days=5))
    
    dfsliced= df1[five_days_before_str:date_str]
    
    row_count= dfsliced.shape[0]
    
    if(row_count >0):
        row_index=row_count-1   
   
        
        return dfsliced.ix[row_index].name
    else:
        return df1.ix[0].name 
