UPDATE df_technicals,(
SELECT symbol,
MAX(high) AS high_max,
MIN(high) AS high_min,
AVG(high) AS high_median, 
MAX(low) AS low_max ,
MIN(low) AS low_min ,
AVG(low) AS low_median 
FROM history_symbol 

WHERE DATE >=(SELECT DATE FROM historicaldates WHERE datetype='5days')
GROUP BY symbol)AS temp
SET
df_technicals.low_5day_max=temp.low_max,
df_technicals.low_5day_min=temp.low_min,
df_technicals.low_5day_median=temp.low_median,

df_technicals.high_5day_max=temp.high_max,
df_technicals.high_5day_min=temp.high_max,
df_technicals.high_5day_median=temp.high_median
WHERE df_technicals.symbol=temp.symbol