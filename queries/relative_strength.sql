
UPDATE technicals_symbol t,(
SELECT t1.symbol,(t1.year_change-t2.year_change) AS relative_strength FROM 
(
SELECT symbol,(100*(CLOSE-price_Yearly))/price_Yearly AS year_change FROM df_technicals

)
AS t1
JOIN

(
SELECT symbol,(100*(CLOSE-price_Yearly))/price_Yearly AS year_change FROM df_technicals
WHERE symbol ='SPY'
)
AS t2) temp


SET t.relative_strength=temp.relative_strength
WHERE t.symbol=temp.symbol
