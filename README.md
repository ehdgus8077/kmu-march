# Enron 회사 이메일 데이터 분석

Enron 이라는 미국의 에너지 회사의 이메일 데이터를 가공하여 DB에 정형화된 형태로 저장한 후, 
정형화된 데이터를 사용하여 여러 가지 정보를 추출한다.
* 학습용


## 코드 사용방법

### Data Parsing
 - "python3 parser.py" 입력.
 - "data.csv" 파일이 kmu-march와 동일한 위치에 저장된다.

### DB 초기화
 - mysql 설치되어 있다고 가정.
 - .env 를 작성한다.(mysql 권한 설정을 하고, 컬럼이 너무 길다는 에러를 발생할 시, "SET global.sql_mode= '';" 을 설정한다.
 - "python3 mysql.py" 입력.
 - "Enron" DB를 생성 후, 그 안에 "email", "emailTo" table을 생성한다.

### Data Engineering
 - "python3 engineering.py" 입력.
 - "data.csv" 파일을 이용하여 알맞게 DB에 삽입한다.

### Data analysis
 - "python3 analysis.py" 입력.
 - 문제에 대한 답 출력
