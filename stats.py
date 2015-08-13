from bl import stats_manager 
from dao import dbdao
from util import loglib

logger = loglib.getlogger('stats')
list_symbol=dbdao.get_symbols_list()
dbdao.execute_query(["Delete from fin_stats_symbol"])

for symbol in list_symbol:
    list_function=[stats_manager.get_IncomeStatement(symbol),stats_manager.get_BalanceSheet(symbol),stats_manager.get_CashFlow(symbol)]
    for function_name in list_function:
        function_name 
