import pandas as pd
from dao import dbdao

df=pd.read_csv('data/synopsis/synopsis_rules.csv')
print df    
df.set_index("rule_id",inplace=True)
dbdao.save_dataframe(df, "synopsis_rule")