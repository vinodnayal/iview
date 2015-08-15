import pandas as pd
from dao import dbdao
from mock import inplace

df=dbdao.get_data_db_frame("select * from fin_stats_symbol")

df.set_index('Item',inplace=True)
#df=df.transpose()

print df


exit()


dbdao.save_dataframe(df, "temp_fun")

# df.to_csv("data/stats/cash_flow/AA1.csv")
print df