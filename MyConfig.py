import ConfigParser


class MyConfig:
    
        cfg = ConfigParser.ConfigParser()
        cfg.read("config.ini")
        mongodb_host = cfg.get("Connections", "mongodb_host")
        mongodb_port = cfg.getint("Connections", "mongodb_port")
        
        mysqldb_host = cfg.get("Connections", "mysqldb_host")
        mysqldb_port = cfg.getint("Connections", "mysqldb_port")
        mysqldb_user = cfg.get("Connections", "mysqldb_user")
        mysqldb_passwd = cfg.get("Connections", "mysqldb_pwd")
        mysqldb_db = cfg.get("Connections", "mysqldb_db")
        
        start_time = cfg.get("Timezone", "start_time")
        end_time = cfg.get("Timezone", "end_time")
        list_of_holidays = cfg.get("Timezone", "list_of_holidays")
        data_pull_interval = cfg.get("Timezone", "data_pull_interval")
        logpath = cfg.get("FileSystem", "logpath")

        
        gmail_user_1 = cfg.get("Email", "gmail_user_1")
        gmail_pwd_1 = cfg.get("Email", "gmail_pwd_1")
        gmail_user_2 = cfg.get("Email", "gmail_user_2")
        gmail_pwd_2 = cfg.get("Email", "gmail_pwd_2")
