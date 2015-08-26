import numpy
import talib
from talib import MA_Type
import numpy as np
from talib import abstract
from dao import dbdao,mongodao
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy.misc import derivative
import dao.mongodao as mongodao
import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd

from util import loglib

import csv
from util import constants
import os
from bl import technical_manager

def process(x):
    x=(str) (x)
    return (int)(x.replace('-',''))
end_date_time = datetime.datetime.now()  # mysqldb.get_maxdate()[0]   
start_date_time = end_date_time - relativedelta(days=constants.DAYS_FOR_TECHNICALS)
  
days_behind=100
 
df_mkt=mongodao.getsymbol_data_temp(constants.MKT_SYMBOL, start_date_time, end_date_time)

print df_mkt.to_html()

exit()
df_mkt['date']=df_mkt.index

y=df_mkt['close'].as_matrix()
x=df_mkt['date'].apply(process).as_matrix()

print x
f2 = interp1d(x, y)
xnew = np.arange(20140102, 300, 1)
# df_dx = derivative(f2, xnew)
# print df_dx
# exit()


plt.plot(x, y, 'o', xnew, f2(xnew), '-', xnew, f2(xnew), '--')
plt.legend(['data', 'linear', 'cubic'], loc='best')
plt.show()




