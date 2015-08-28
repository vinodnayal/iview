update industry_new as t2 , industries as t1
set t2.id=t1.industryid
where 
replace(replace(upper(substring(t1.industryname,1,20)),"-","")," ","") = 
replace(replace(replace(upper(substring(t2.name,1,20)),"\n",""),"-","")," ","")

and t2.id is null