UPDATE df_technical t,

(
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
t.low_5day_max=temp.low_max,
t.low_5day_min=temp.low_min,
t.low_5day_median=temp.low_median,

t.high_5day_max=temp.high_max,
t.high_5day_min=temp.high_min,
t.high_5day_median=temp.high_median
WHERE t.symbol=temp.symbol;


-- rsi text update
update df_technical,ctratingvalues
set rsi_text=ctratingtext

where df_technical.rsi_value=ctratingvalues.ctrating;

-- std50days


update df_technical

set std50days =(close-sma50)/(close*stddev);
