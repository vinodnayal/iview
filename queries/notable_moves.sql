delete from temp_notable;
    
INSERT INTO temp_notable (symbol,typeid,per_change) 
SELECT temp1.symbol,typeid,temp1.per_change FROM
(SELECT h1.symbol,h1.open,h2.high,100*((h2.high-h1.open)/h1.open) AS per_change FROM 
((SELECT * FROM history_symbol WHERE DATE = (SELECT DATE FROM historicaldates WHERE DateType='current') AND OPEN >1 )AS h1
JOIN 
(SELECT * FROM history_symbol WHERE DATE = (SELECT DATE FROM historicaldates WHERE DateType='PreviousDay') AND OPEN >1 )AS h2
ON h1.symbol=h2.symbol   )) AS temp1,
notable_moves_types 
WHERE Name="Full Gap Up" AND per_change>0
ORDER BY  ABS(temp1.per_change) DESC 
LIMIT 10;

INSERT INTO temp_notable (symbol,typeid,per_change) 
SELECT temp1.symbol,typeid,temp1.per_change FROM
(SELECT h1.symbol,h1.open,h2.high,100*((h2.low-h1.open)/h1.open) AS per_change FROM 
((SELECT * FROM history_symbol WHERE DATE = (SELECT DATE FROM historicaldates WHERE DateType='current') AND OPEN >1 )AS h1
JOIN 
(SELECT * FROM history_symbol WHERE DATE = (SELECT DATE FROM historicaldates WHERE DateType='PreviousDay') AND OPEN >1 )AS h2
ON h1.symbol=h2.symbol   )) AS temp1,
notable_moves_types 
WHERE NAME='Full Gap Down' AND per_change<0
ORDER BY  ABS(temp1.per_change) DESC 
LIMIT 10;



INSERT INTO temp_notable (symbol,typeid,per_change) 
SELECT temp1.symbol,typeid,temp1.per_change FROM
(SELECT h1.symbol,h1.open,h2.close,100*((h2.close-h1.open)/h1.open) AS per_change FROM 
((SELECT * FROM history_symbol WHERE DATE = (SELECT DATE FROM historicaldates WHERE DateType='current') AND OPEN >1 )AS h1
JOIN 
(SELECT * FROM history_symbol WHERE DATE = (SELECT DATE FROM historicaldates WHERE DateType='PreviousDay') AND OPEN >1 )AS h2
ON h1.symbol=h2.symbol   )) AS temp1,
notable_moves_types 
WHERE NAME='Partial Gap up' AND per_change>0
ORDER BY  ABS(temp1.per_change) DESC 
LIMIT 10;

INSERT INTO temp_notable (symbol,typeid,per_change) 
SELECT temp1.symbol,typeid,temp1.per_change FROM
(SELECT h1.symbol,h1.open,h2.close,100*((h2.close-h1.open)/h1.open) AS per_change FROM 
((SELECT * FROM history_symbol WHERE DATE = (SELECT DATE FROM historicaldates WHERE DateType='current') AND OPEN >1 )AS h1
JOIN 
(SELECT * FROM history_symbol WHERE DATE = (SELECT DATE FROM historicaldates WHERE DateType='PreviousDay') AND OPEN >1 )AS h2
ON h1.symbol=h2.symbol)) AS temp1,
notable_moves_types 
WHERE NAME="Partial Gap Down" AND per_change<0
ORDER BY  ABS(temp1.per_change) DESC 
LIMIT 10;


INSERT INTO temp_notable (symbol,typeid,per_change)
SELECT t1.symbol,t2.typeid,(100*(t1.LAST-t1.52weekhigh)/t1.52weekhigh) AS per_change FROM live_symbol AS t1
JOIN notable_moves_types AS t2
WHERE (100*(t1.LAST-t1.52weekhigh)/t1.52weekhigh)>0 AND t2.NAME="New High"
ORDER BY ABS(per_change) DESC
LIMIT 10;


INSERT INTO temp_notable (symbol,typeid,per_change)
SELECT t1.symbol,t2.typeid,(100*(t1.LAST-t1.52weeklow)/t1.52weeklow) AS per_change FROM live_symbol AS t1
JOIN notable_moves_types AS t2
WHERE (100*(t1.LAST-t1.52weeklow)/t1.52weeklow)<0 AND t2.NAME="New Low"
ORDER BY ABS(per_change) DESC
LIMIT 10;

INSERT INTO temp_notable (symbol,typeid)
SELECT t1.symbol,t2.typeid FROM
(SELECT symbol, rsi FROM technical_symbol_history WHERE DATE = (SELECT DATE FROM historicaldates WHERE DateType="current")) AS t1
JOIN notable_moves_types AS t2
WHERE t2.NAME="Most Overbought"
ORDER BY t1.rsi DESC
LIMIT 10;

INSERT INTO temp_notable (symbol,typeid)
SELECT t1.symbol,t2.typeid FROM
(SELECT symbol, rsi FROM technical_symbol_history WHERE DATE = (SELECT DATE FROM historicaldates WHERE DateType="current")) AS t1
JOIN notable_moves_types AS t2
WHERE t2.NAME="Most Oversold"
ORDER BY t1.rsi ASC
LIMIT 10;


INSERT INTO temp_notable (symbol,typeid,per_change)
SELECT t1.symbol,t2.typeid,t1.change_pct AS per_change FROM live_symbol AS t1
JOIN notable_moves_types AS t2
WHERE t1.change_pct>0 AND NAME="Top Performer"
ORDER BY ABS(t1.change_pct) DESC
LIMIT 10;

INSERT INTO temp_notable (symbol,typeid,per_change)
SELECT t1.symbol,t2.typeid,t1.change_pct AS per_change FROM live_symbol as t1
JOIN notable_moves_types AS t2
WHERE change_pct<0 and NAME="Bottom Performer"
ORDER BY ABS(t1.change_pct) DESC
LIMIT 10;


INSERT INTO temp_notable (symbol,typeid,per_change)
    SELECT h.symbol,n.typeid,(100*(h.volume -l.volume)/(l.volume)) AS per_change FROM history_symbol AS h
    JOIN symbol_avg_volume AS l 
    ON h.symbol=l.symbol
    JOIN notable_moves_types AS n
    WHERE DATE = (SELECT DATE FROM historicaldates WHERE DateType='current')
    AND (100*(h.volume -l.volume)/(l.volume))>0
    AND n.name="New Positive Volume"
    ORDER BY ABS(per_change) DESC
    LIMIT 10;


INSERT INTO temp_notable (symbol,typeid,per_change)
    SELECT h.symbol,n.typeid,(100*(h.volume -l.volume)/(l.volume)) AS per_change FROM history_symbol AS h
    JOIN symbol_avg_volume AS l 
    ON h.symbol=l.symbol
    JOIN notable_moves_types AS n
    WHERE DATE = (SELECT DATE FROM historicaldates WHERE DateType='current')
    AND (100*(h.volume -l.volume)/(l.volume))<0
    AND n.name="New Negative Volume"
    ORDER BY ABS(per_change) DESC
    LIMIT 10;