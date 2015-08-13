from bl import news_manager

from util import loglib


logger = loglib.getlogger('news')

logger.info("Retrieving news from all sources")
filepath='data/news/ALL_NEWS.csv'
news_manager.save_NEWS(filepath)
logger.info("saved all news")







