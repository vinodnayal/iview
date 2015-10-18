

-- Full Gap queries
    
create table temp_notable as

SELECT temp1.symbol,typeid,temp1.per_change FROM
(
SELECT h1.date as cdate,h2.date as pdate, h1.symbol,h1.open,h2.high,100*((h1.open-h2.high)/h2.high) AS per_change FROM 
(
(SELECT * FROM history_spysymbol WHERE DATE = (SELECT DATE FROM historicaldates WHERE DateType='current') AND close >1 )AS h1
JOIN 
(SELECT * FROM history_spysymbol WHERE DATE = (SELECT DATE FROM historicaldates WHERE DateType='PreviousDay') AND close >1 )AS h2

ON h1.symbol=h2.symbol   )
) AS temp1,
notable_moves_types 
WHERE Name="Full Gap Up" AND per_change>0 and  per_change<100
ORDER BY  ABS(temp1.per_change) DESC 
LIMIT 10;


INSERT INTO temp_notable (symbol,typeid,per_change) 
SELECT temp1.symbol,typeid,temp1.per_change FROM
(SELECT h1.symbol,h1.open,h2.high,100*((h1.open-h2.low)/h2.low) AS per_change FROM 
((SELECT * FROM history_spysymbol WHERE DATE = (SELECT DATE FROM historicaldates WHERE DateType='current') AND close >1 )AS h1
JOIN 
(SELECT * FROM history_spysymbol WHERE DATE = (SELECT DATE FROM historicaldates WHERE DateType='PreviousDay') AND close >1 )AS h2
ON h1.symbol=h2.symbol   )) AS temp1,
notable_moves_types 
WHERE NAME='Full Gap Down' AND per_change<0 and per_change>-100
ORDER BY  temp1.per_change asc 
LIMIT 10;



INSERT INTO temp_notable (symbol,typeid,per_change) 

SELECT temp1.symbol,typeid,temp1.per_change FROM
(
SELECT h1.date as cdate,h2.date as pdate, h1.symbol,h1.open,h2.high,100*((h1.open-h2.close)/h2.close) AS per_change FROM 
(
(SELECT * FROM history_spysymbol WHERE DATE = (SELECT DATE FROM historicaldates WHERE DateType='current') AND close >1 )AS h1
JOIN 
(SELECT * FROM history_spysymbol WHERE DATE = (SELECT DATE FROM historicaldates WHERE DateType='PreviousDay') AND close >1 )AS h2

ON h1.symbol=h2.symbol   )
) AS temp1,
notable_moves_types 
WHERE Name="Partial Gap up" AND per_change>0 and  per_change<100
ORDER BY  ABS(temp1.per_change) DESC 
LIMIT 10;

INSERT INTO temp_notable (symbol,typeid,per_change) 
SELECT temp1.symbol,typeid,temp1.per_change FROM
(SELECT h1.symbol,h1.open,h2.high,100*((h1.open-h2.close)/h2.close) AS per_change FROM 
((SELECT * FROM history_spysymbol WHERE DATE = (SELECT DATE FROM historicaldates WHERE DateType='current') AND close >1 )AS h1
JOIN 
(SELECT * FROM history_spysymbol WHERE DATE = (SELECT DATE FROM historicaldates WHERE DateType='PreviousDay') AND close >1 )AS h2
ON h1.symbol=h2.symbol   )) AS temp1,
notable_moves_types 
WHERE NAME='Partial Gap Down' AND per_change<0 and per_change>-100
ORDER BY  temp1.per_change asc 
LIMIT 10;



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

-- over bought sold

INSERT INTO temp_notable (symbol,typeid)
SELECT t1.symbol,t2.typeid FROM
(SELECT symbol, rsi FROM technicals_symbol ) AS t1
JOIN notable_moves_types AS t2
join spy_symbol t3 
on t1.symbol=t3.symbol
WHERE t2.NAME="Most Overbought"
ORDER BY t1.rsi DESC
LIMIT 10;


INSERT INTO temp_notable (symbol,typeid)
SELECT t1.symbol,t2.typeid FROM
(SELECT symbol, rsi FROM technicals_symbol ) AS t1
JOIN notable_moves_types AS t2
join spy_symbol t3 
on t1.symbol=t3.symbol
WHERE t2.NAME="Most OverSold"
ORDER BY t1.rsi ASC
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



-- avg volume




delete from symbol_avg_volume;
insert into  symbol_avg_volume(symbol,volume)
select symbol,avg(volume) from history_spysymbol where date >='2015-05-01' and volume > 1000 group by symbol  ; 


INSERT INTO temp_notable (symbol,typeid,per_change)
SELECT h.symbol,n.typeid,(100*(h.volume -l.volume)/(l.volume)) AS per_change FROM history_spysymbol AS h
    JOIN symbol_avg_volume AS l 
    ON h.symbol=l.symbol
    JOIN notable_moves_types AS n
    WHERE DATE = (SELECT DATE FROM historicaldates WHERE DateType='current')
    AND (100*(h.volume -l.volume)/(l.volume))>0 and h.close>1 and h.volume > 10000 and l.volume > 10000
    AND n.name="Positive Volume"
    ORDER BY per_change DESC
    LIMIT 10;



    INSERT INTO temp_notable (symbol,typeid,per_change)

    SELECT h.symbol,n.typeid,(100*(h.volume -l.volume)/(l.volume)) AS per_change FROM history_spysymbol AS h
    JOIN symbol_avg_volume AS l 
    ON h.symbol=l.symbol
    JOIN notable_moves_types AS n
    WHERE DATE = (SELECT DATE FROM historicaldates WHERE DateType='current')
    AND (100*(h.volume -l.volume)/(l.volume))<0 and  h.close>1 and  h.volume > 10000 and l.volume > 10000
    AND n.name="Negative Volume"
    ORDER BY ABS(per_change) DESC
    LIMIT 10;



-- cross overs

insert into temp_notable (symbol,typeid,per_change) 
SELECT t1.symbol,20 as typeid,100*(t1.last-sma200)/sma200  AS PER_CHANGE FROM live_symbol t1 
join technicals_symbol t2 
on t1.symbol=t2.symbol
join spy_symbol t3

on t1.symbol=t3.symbol
where 100*(t1.last-sma200)/sma200 >0  and t1.last >1 and 100*(t1.last-sma200)/sma200 < 100 
order by 100*(t1.last-sma200)/sma200 desc  limit 10;


insert into temp_notable (symbol,typeid,per_change) 

SELECT t1.symbol,21 as typeid,100*(t1.last-sma200)/sma200  AS PER_CHANGE FROM live_symbol t1 
join technicals_symbol t2 
on t1.symbol=t2.symbol
join spy_symbol t3
on t1.symbol=t3.symbol

where 100*(t1.last-sma200)/sma200 < 0  and t1.last >1 and 100*(t1.last-sma200)/sma200 > -100 
order by 100*(t1.last-sma200)/sma200 asc  limit 10;



insert into temp_notable (symbol,typeid,per_change) 
SELECT t1.symbol,22 as typeid,100*(t1.last-sma50)/sma50  AS PER_CHANGE FROM live_symbol t1 
join technicals_symbol t2 
on t1.symbol=t2.symbol
join spy_symbol t3
on t1.symbol=t3.symbol
where 100*(t1.last-sma50)/sma50 >0  and t1.last >1 and 100*(t1.last-sma50)/sma50 < 100 
order by 100*(t1.last-sma50)/sma50 desc  limit 10;




insert into temp_notable (symbol,typeid,per_change) 

SELECT t1.symbol,23 as typeid,100*(t1.last-sma50)/sma50  AS PER_CHANGE FROM live_symbol t1 
join technicals_symbol t2 
on t1.symbol=t2.symbol
join spy_symbol t3
on t1.symbol=t3.symbol
where 100*(t1.last-sma50)/sma50 < 0  and t1.last >1 and 100*(t1.last-sma50)/sma50 > -100 
order by 100*(t1.last-sma50)/sma50 asc  limit 10;



-- relative stength

insert into temp_notable (symbol,typeid,per_change) 
select t1.symbol,17,relative_strength from technicals_symbol  t1
join spy_symbol t2
on t1.symbol=t2.symbol
where relative_strength > 0 
order by relative_strength desc
limit 10;


delete from notable_moves_symbol;


insert into notable_moves_symbol(symbol,type,per_change)

select symbol,typeid,per_change from temp_notable;

drop table temp_notable;









