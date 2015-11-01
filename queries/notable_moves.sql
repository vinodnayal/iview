-- new high low 

INSERT INTO temp_notable (symbol,typeid,per_change)
SELECT t1.symbol,t2.typeid,(100*(t1.LAST-t1.52weekhigh)/t1.52weekhigh) AS per_change FROM live_symbol AS t1
join list_symbol as t3 
on t1.symbol=t3.symbol
JOIN notable_moves_types AS t2
WHERE (100*(t1.LAST-t1.52weekhigh)/t1.52weekhigh)>0 AND t2.NAME="New High" and t1.last >1 and t3.isactive=1
ORDER BY ABS(per_change) DESC
LIMIT 10;


INSERT INTO temp_notable (symbol,typeid,per_change)
SELECT t1.symbol,t2.typeid,(100*(t1.LAST-t1.52weeklow)/t1.52weeklow) AS per_change FROM live_symbol AS t1
join list_symbol as t3 
on t1.symbol=t3.symbol
JOIN notable_moves_types AS t2
WHERE (100*(t1.LAST-t1.52weeklow)/t1.52weeklow)<0 AND t2.NAME="New Low" and t1.last >1 and t3.isactive=1
ORDER BY ABS(per_change) DESC
LIMIT 10;


-- top and bottom performer


INSERT INTO temp_notable (symbol,typeid,per_change)
SELECT t1.symbol,t2.typeid,t1.change_pct_value AS per_change FROM live_symbol AS t1
join spy_symbol as s
on t1.symbol=s.symbol
JOIN notable_moves_types AS t2
WHERE t1.change_pct_value>0  and t1.change_pct_value<100 AND t1.last > 1 and t2.NAME="Top Performer"
ORDER BY ABS(t1.change_pct_value) DESC
LIMIT 10;

INSERT INTO temp_notable (symbol,typeid,per_change)
SELECT t1.symbol,t2.typeid,t1.change_pct_value AS per_change FROM live_symbol as t1
join spy_symbol as s
on t1.symbol=s.symbol
JOIN notable_moves_types AS t2
WHERE change_pct_value<0 and t2.NAME="Bottom Performer" and  t1.change_pct_value>-100 AND t1.last > 1
ORDER BY ABS(t1.change_pct_value) DESC
LIMIT 10;






 
 
 

delete from notable_moves_symbol;


insert into notable_moves_symbol(symbol,type,per_change)

select symbol,typeid,per_change from temp_notable;

drop table temp_notable;









