UPDATE df_technical t,(
SELECT t1.symbol,round((t1.year_change-t2.year_change),2) AS relative_strength FROM 
(
SELECT symbol,(100*(CLOSE-price_Yearly))/price_Yearly AS year_change FROM df_technical

)
AS t1
JOIN

(
SELECT symbol,(100*(CLOSE-price_Yearly))/price_Yearly AS year_change FROM df_technical
WHERE symbol ='SPY'
)
AS t2) temp


SET t.relative_strength=temp.relative_strength
WHERE t.symbol=temp.symbol