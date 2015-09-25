from dao import dbdao
from util import df_util

dbdao.execute_query(["delete from df_stats_quarter"])
df=df_util.create_dataframe("data\\stats\\balance_sheet","Symbol", "Balance Sheet","df_stats_quarter")

df=df_util.create_dataframe("data\\stats\\income_statement","Symbol", "Income Statement","df_stats_quarter")

df=df_util.create_dataframe("data\\stats\\cash_flow","Symbol", "Cash Flow","df_stats_quarter")




