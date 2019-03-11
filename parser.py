import os, csv

DATA_PATH = "../emails"
CSV_PATH = "../data.csv"
TYPE_LIST = [
             'Message-ID', 'Date', 'From', 'To',
             'Subject', 'Cc', 'Mime-Version', 'Content-Type',
             'Content-Transfer-Encoding', 'Bcc', 'X-From', 'X-To',
             'X-cc', 'X-bcc', 'X-Folder', 'X-Origin', 'X-FileName'
             ]

def headerToDict(headerList):
  dict = {}
  preKey = ""
  for key in TYPE_LIST:
    dict[key] = "NULL"

  for header in headerList:
    
    if header[0] == " " or ": " not in header:
      dict[preKey] += header
      continue

    tempList = header.split(": ")
    dict[tempList[0]] = tempList[1]
    if dict[tempList[0]] == " ":
      dict[tempList[0]] = "NULL"

    preKey = tempList[0]
  
  return dict

def getHeader(filePath):
  headerList = []
  with open(filePath, "r") as fr:
    while True:
      line = fr.readline().replace("\n" ,"")
      if not line or line == "": 
        break
      headerList.append(line)
  return headerList


if __name__ == "__main__":
  
  dataList = []

  for filename in os.listdir(DATA_PATH):
    full_filename = os.path.join(DATA_PATH, filename)
    dataList.append(headerToDict(getHeader(full_filename)))