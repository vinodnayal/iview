select * from df_etf_load t1
join symbol_fundamental t2 on
t1.symbol=t2.symbol
 where
name not like '%ishares%' and
name not like '%ETF%' and
name not like '%Portfolio%' and 
name not like '%X-trackers%' and 
name not like '%SPDR%' and 
name not like '%Hedge%' and 
name not like '%Growth%' and 
name not like '%Yield%'  and 
name not like '%Tactical%'  and 
name not like '%proshares%'  and 
name not like '%Vanguard%' and 
name not like '%trust%' and 
name not like '%powershares%' and 
name not like '%global%' 
;

*****************************************************************************************
update 
symbol_fundamental 
set asset='US Equities',
asset_detail='US Equities'
where sector <> ''
and asset is  null
************************************************************


update symbol_fundamental t1 ,symbol_live_yahoo  t2
set t1.asset_detail='LargeCap'
where  t1.symbol=t2.symbol and
t2.market_Cap >=10000000000;


update symbol_fundamental t1 ,symbol_live_yahoo  t2
set t1.asset_detail='MidCap'
where  t1.symbol=t2.symbol and
t2.market_Cap >=2000000000 and 
t2.market_Cap < 10000000000;


update symbol_fundamental t1 ,symbol_live_yahoo  t2
set t1.asset_detail='SmallCap'
where  t1.symbol=t2.symbol and
t2.market_Cap <2000000000 and t2.market_Cap > 1000;

update symbol_fundamental t1 ,symbol_live_yahoo  t2
set t1.asset_detail=''
where  t1.symbol=t2.symbol and
t2.market_Cap =0;
*************************************************

*****************************************************************

 update symbol_fundamental t1 , df_etf_load t2
 set t1.asset_detail=t2.asset
 where t1.symbol=t2.symbol
 
 *****************************************************************
 OTC Symbols
 
 update symbol_fundamental
set asset='OTC'
where asset is null and asset_detail='SmallCap'
 
 