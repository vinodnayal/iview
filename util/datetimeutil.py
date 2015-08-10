import datetime
def getdatetime(date):
    return datetime.datetime(date.year, date.month, date.day, 0, 0, 0)

def getdate(datetime):
    return datetime.date()
    
def getdatewithzero(datetime):
    return getdatetime(datetime.date())

def getcurtimestr():
    return datetime.datetime.now().strftime("%Y%m%d%I%M%S")    
def getdatefromstr(strdate):
    
    return datetime.datetime.strptime(strdate, '%Y-%m-%d')

def getdatestr(date):
    return date.strftime("%Y-%m-%d") 