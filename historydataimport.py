from datetime import timedelta
import datetime
from pandas.io.data import DataReader
import logging.config 
from MyConfig import MyConfig as cfg

import traceback


from util import loglib
from bl.import_data import dataimport
from dao import dbdao

logger = loglib.getlogger('historicaldataimport')

import sys


dataimport.importdata(dbdao.get_symbols_list())        