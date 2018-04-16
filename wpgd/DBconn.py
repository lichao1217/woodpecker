import pymysql
import configparser
import os

"""
创建连接数据库的类
"""
class DBConn(object):
    _configPath = ""
    _config = None
    def __init__(self):
        base_dir = os.getcwd()
        self._configPath = base_dir+r"\config.ini"
        
        
    def __get_dbconn(self):
        try:
           
            _config = configparser.ConfigParser()
            _config.read(self._configPath)
            host = _config.get("dbconfig","host")
            dbusername = _config.get("dbconfig","dbusername")
            dbuserpwd = _config.get("dbconfig","dbuserpwd")
            dbname = _config.get("dbconfig","dbname")
            db = pymysql.connect(host,dbusername,dbuserpwd,dbname)
            return db
        except Exception as e:
            return None

    def get_serverList(self,sqltext):
        db = self.__get_dbconn()
        if db is None:
            return 0  #0表示连接数据库失败
        else :
            try:
                cursor = db.cursor()
                cursor.execute(sqltext)
                results = cursor.fetchall()
                return results
            except Exception as e:
                return -1 # -1 表示读取数据失败，有可能SQL语句不对
            finally :
                db.close()
                
    def writeDB(self,sqltext):
        db = self.__get_dbconn()
        if db is None:
            return 0  #0表示连接数据库失败
        else :
            try:
                cursor = db.cursor()
                cursor.execute(sqltext)
                db.commit()
                return 1 #1表示插入数据成功
            except Exception as e:
                db.rollback()
                return -1 # -1 插入数据失败
            finally :
                db.close()
        
