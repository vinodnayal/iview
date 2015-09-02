from dao import dbdao
from util import loglib


logger = loglib.getlogger('notable moves')

f=open('queries/notable_moves.sql')

queries=f.read().strip().split(';')

print len(queries)

#last query is empty
queries=queries[:len(queries)-1]

dbdao.execute_query(queries)