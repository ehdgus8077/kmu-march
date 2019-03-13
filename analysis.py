from mysql import MysqlMgr

def quiz_1(mysql):

  print("""
        * How many emails did each person receive each day?
        """)
  sql = """SELECT DATE_FORMAT( email.Date, '%Y%m%d' ), emailTo.addressTo ,  count(1) count FROM email join emailTo on 
            email.MessageID = emailTo.MessageID
           GROUP BY DATE_FORMAT( email.Date, '%Y%m%d' ), emailTo.addressTo
        """
  results = mysql.selectQuery(sql)

  resultDict = {}
  for result in results:
    if result[0] in resultDict:
      resultDict[result[0]].append([result[1], result[2]])
    else :
      resultDict[result[0]] = [ [result[1], result[2]] ]

  for date in resultDict:
    print(f"[{date}]")
    for info in resultDict[date]:
      print(f"{info[0]} - {info[1]}")

def quiz_2(mysql):

  print("""
        *  Let's label an email as "direct" if there is exactly
           one recipient and "broadcast" if it has multiple recipients.
           Identify the person (or people) who received the largest number of direct
           emails and the person (or people)
           who sent the largest number of broadcast emails.
        """)

  sql = """SELECT email.addressFrom, count(1) count FROM email join emailTo on 
            email.MessageID = emailTo.MessageID
           GROUP BY email.addressFrom, email.MessageID HAVING count > 1
        """
  results = mysql.selectQuery(sql)
  
  broadcastDict = {}
  directDict = {}

  for result in results:
    if result[0] == "NULL":
      continue
    if result[0] in broadcastDict:
      broadcastDict[result[0]] += 1
    else:
      broadcastDict[result[0]] = 1

  
  for result in mysql.selectQuery(sql.replace(">" ,"=")):
    if result[0] == "NULL":
      continue
    if result[0] in directDict:
        directDict[result[0]] += 1
    else:
      directDict[result[0]] = 1

  directDict = sorted(directDict.items(), key=lambda kv: kv[1], reverse=True)
  broadcastDict = sorted(broadcastDict.items(), key=lambda kv: kv[1], reverse=True)

  temp = broadcastDict[0][1]
  print("[broadcast]")
  for idx in range(len(broadcastDict)):
    if temp != broadcastDict[idx][1]:
      break
    print(f"{broadcastDict[idx][0]} - {broadcastDict[idx][1]}")
    
  temp = directDict[0][1]
  print("[directDict]")
  for idx in range(len(directDict)):
    if temp != directDict[idx][1]:
      break
    print(f"{directDict[idx][0]} - {directDict[idx][1]}")
    

def quiz_3(mysql):

  print("""
      *  Find the five emails with the fastest response times.
          (A response is defined as a message from one of the
          recipients to the original sender whose subject line
          contains all of the words from the subject of the original email,
          and the response time should be measured as the difference between
          when the original email was sent and when the response was sent.)
      """)

  sql = "SELECT * from email"

  results = mysql.selectQuery(sql)
  Dict = {}
  for result in results:
    key = result[1].replace("re","").replace("Re","").replace("RE","")
    if key in Dict:
      Dict[key].append(result)
    else:
      Dict[key] = [result]

  timeDict = {} 
  for subject in Dict:
    Dict[subject].sort(key = lambda element : element[-2])
    for t in range(len(Dict[subject])):
      for f in range(t + 1, len(Dict[subject])):
        if(Dict[subject][t][1][:3].lower() != "re:"):
          continue
        if Dict[subject][t][-2] + 1 == Dict[subject][f][-2]:

          result1 = mysql.selectQuery(f'SELECT MessageID FROM emailTo WHERE MessageID = "{Dict[subject][t][0]}" AND addressTo = "{Dict[subject][f][2]}" ' )
          result2 = mysql.selectQuery(f'SELECT MessageID FROM emailTo WHERE MessageID = "{Dict[subject][f][0]}" AND addressTo = "{Dict[subject][t][2]}" ')
          if len(result1) == 0 or len(result2) == 0:
            continue

          if Dict[subject][f][-1] <= Dict[subject][t][-1]:
            continue
          
          timeDict[Dict[subject][f][0]] =  Dict[subject][f][-1] - Dict[subject][t][-1]
  for info in sorted(timeDict.items(), key=lambda kv: kv[1])[:5]:
    print(f"{info[0]} - {info[1]}")

if __name__ == "__main__":
  mysql = MysqlMgr()
  quiz_1(mysql)
  quiz_2(mysql)
  quiz_3(mysql)
  