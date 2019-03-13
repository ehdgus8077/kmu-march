from mysql import MysqlMgr
from parser import Parser

if __name__ == "__main__":
  parser = Parser()
  mysql = MysqlMgr()
  dictList = parser.csvTodictList("../data.csv")

  for Dict in dictList:
    mysql.insertData(Dict)

  