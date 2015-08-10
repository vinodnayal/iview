import logging.handlers

def getlogger(name):
    return getloggerWithFile(name, 'newlog.txt')

def getloggerWithFile(name, filename):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)  
    filename ="logs/"+filename
    # create a file handler
    handler = logging.handlers.RotatingFileHandler(filename, mode='a', maxBytes=100000000, backupCount=20)
    # handler = logging.FileHandler('hello.log')
    handler2 = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    handler2.setLevel(logging.INFO)
    
    # create a logging format
    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    handler2.setFormatter(formatter)
    logger.addHandler(handler)
    logger.addHandler(handler2)
    return logger
