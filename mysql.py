import dotenv 
import pymysql.cursors
from datetime import datetime

ENVS = dotenv.dotenv_values("./.env")

REAL_TYPE_LIST = [ 'Message-ID', 'Subject', 'From', 'ReplyCnt', 'Date']

class MysqlMgr:
  
  def __init__(self):
    self.host = ENVS["HOST"]
    self.user = ENVS["USER"]
    self.pwd = ENVS["PWD"]
    self.dbName = "Enron"
    
  def createDB(self):
    conn = pymysql.connect(host=self.host,
            user=self.user,
            password=self.pwd,
            charset='utf8mb4')
    
    try:
      with conn.cursor() as cursor:
          sql = f"CREATE DATABASE {self.dbName}"
          cursor.execute(sql)
      conn.commit()
    finally:
      conn.close()

  def deleteDB(self):
    conn = pymysql.connect(host=self.host,
            user=self.user,
            password=self.pwd,
            charset='utf8mb4')
    
    try:
      with conn.cursor() as cursor:
          sql = f"DROP DATABASE {self.dbName}"
          cursor.execute(sql)
      conn.commit()
    finally:
      conn.close()
  
  def createTable(self):

    conn = pymysql.connect(host=self.host,
        user=self.user,
        password=self.pwd,
        db='Enron',
        charset='utf8mb4')
 
    try:
      with conn.cursor() as cursor:
        sql = f"""
              CREATE TABLE email (
                MessageID VARCHAR(255),
                Subject VARCHAR(255),
                addressFrom VARCHAR(255),
                ReplyCnt INT(14),
                Date datetime,
                PRIMARY KEY(MessageID)
                )
              """
        cursor.execute(sql)
        sql = f"""
              CREATE TABLE emailTo (
                IDd INT(14) NOT NULL AUTO_INCREMENT PRIMARY KEY,
                MessageID VARCHAR(255),
                addressTo VARCHAR(255)
                )
              """
        cursor.execute(sql)
        conn.commit()
    finally:
      conn.close()

  def deleteTable(self):

    conn = pymysql.connect(host=self.host,
        user=self.user,
        password=self.pwd,
        db='Enron',
        charset='utf8mb4')
 
    try:
      with conn.cursor() as cursor:
        sql = f"drop table email"
        cursor.execute(sql)
        sql = f"drop table emailTo"
        cursor.execute(sql)
        conn.commit()
    finally:
      conn.close()

  def insertData(self, dataDict):
    conn = pymysql.connect(host=self.host,
        user=self.user,
        password=self.pwd,
        db=self.dbName,
        charset='utf8mb4')
 
    try:
      with conn.cursor() as cursor:
        sql = f"""
              INSERT INTO email (
                MessageID,
                Subject,
                addressFrom,
                ReplyCnt,
                Date
                ) VALUES (
              """

        for key in REAL_TYPE_LIST[:-2]:
          value = dataDict[key].replace('"', '')
          sql += f' "{value}" ,'

        sql += f' "{dataDict["replyCnt"]}" ,'
        times = dataDict["Date"].split(" ")
        dataTime = datetime.strptime("-".join(times[1:5]), "%d-%b-%Y-%H:%M:%S")
        sql += f' "{dataTime}" ) '
        cursor.execute(sql)
        conn.commit()
        
        fromList = []
        for type in ["Cc", 'Bcc', "To"]:
          if dataDict[type] == "NULL":
            continue
          fromList += dataDict[type].split(",")
        fromList = list(set(fromList))
        sql = f"""
                INSERT INTO emailTo (
                  MessageID,
                  addressTo
                )VALUES("{dataDict["Message-ID"]}",
                """

        for From in fromList:  
          From = From.replace('"', '')
          newSql = sql + f'"{From}" )'
          cursor.execute(newSql)
          conn.commit()
    finally:
      conn.close()
  
  def selectQuery(self, query, dict=False):
    conn = pymysql.connect(host=self.host,
        user=self.user,
        password=self.pwd,
        db=self.dbName,
        charset='utf8mb4')

    try:
      if (dict):
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
          cursor.execute(query)
          return cursor.fetchall()
      else:
        with conn.cursor() as cursor:
          cursor.execute(query)
          return cursor.fetchall()
    finally:
      conn.close()
    

if __name__ == "__main__":
  mysqlMgr = MysqlMgr()
  # mysqlMgr.createDB()
  mysqlMgr.deleteTable()
  mysqlMgr.createTable()
  