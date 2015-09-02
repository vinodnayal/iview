from bl import stats_manager 
from dao import dbdao
from util import loglib
import pandas as pd
#dbdao.execute_query(["Delete from fin_stats_symbol"])

import sys
print sys.argv
start,end=sys.argv[1],sys.argv[2]
print start,end
list_symbol=dbdao.get_symbols_list_limit(start, end)
for symbol in list_symbol:
    list_function=[stats_manager.get_IncomeStatement(symbol),stats_manager.get_BalanceSheet(symbol),stats_manager.get_CashFlow(symbol)]
    #list_function=[stats_manager.get_IncomeStatement(symbol)]
    for function_name in list_function:
        function_name 
