import os, csv

DATA_PATH = "../emails"
CSV_PATH = "../data.csv"
TYPE_LIST = [
             'Message-ID', 'Date', 'From', 'To',
             'Subject', 'Cc', 'Mime-Version', 'Content-Type',
             'Content-Transfer-Encoding', 'Bcc', 'X-From', 'X-To',
             'X-cc', 'X-bcc', 'X-Folder', 'X-Origin', 'X-FileName'
             ]

class Parser:

  def headerToDict(self, headerList, replyCnt):

    Dict = {}
    preKey = ""
    for key in TYPE_LIST:
      Dict[key] = "NULL"

    for header in headerList:
      if (header[0] == " ") or (": " not in header):
        Dict[preKey] += header.lstrip()
        continue

      tempList = header.split(": ")
      Dict[tempList[0]] = ": ".join(tempList[1:]).replace("\t", "")
      if Dict[tempList[0]].replace(" ", "") == "":
        Dict[tempList[0]] = "NULL"

      preKey = tempList[0]
    
    Dict["replyCnt"] = replyCnt
    return Dict

  def getHeader(self, filePath):

    headerList = []
    replyCnt = 0
    with open(filePath, "r") as fr:
      lines = fr.readlines()

      for idx in range(len(lines)):
        line = lines[idx].rstrip()
        if line == "":
          for i in range(idx+1,len(lines)):
            if "-----Original Message-----" in lines[i]:
              replyCnt += 1
          break
        headerList.append(line)

    return headerList, replyCnt

  def dictListTocsv(self, dictList):

    keys = dictList[0].keys()

    with open(CSV_PATH, 'w') as output_file:
        dictWriter = csv.DictWriter(output_file, delimiter="\t", fieldnames=keys)
        dictWriter.writeheader()
        dictWriter.writerows(dictList)

  def csvTodictList(self, csvPath):

    dictList = []
    with open(csvPath) as fr:
      dictReader = csv.DictReader(fr, delimiter="\t")

      for message in dictReader:
        dictList.append(dict(message))

      return dictList



if __name__ == "__main__":
  
  parser = Parser()
  dictList = []

  for filename in os.listdir(DATA_PATH):
    full_filename = os.path.join(DATA_PATH, filename)
    headerList, replyCnt = parser.getHeader(full_filename)
    dictList.append(parser.headerToDict(headerList, replyCnt))

  parser.dictListTocsv(dictList)