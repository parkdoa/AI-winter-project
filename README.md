# 🔍이코파인더

- 링크 :[https://main.d1tz93570xd6f8.amplifyapp.com](https://ai-winter-frontend-project.vercel.app/)
&nbsp; 


## 프로젝트 소개

이코파인더는 경제 뉴스 URL 혹은 문장을 복사 붙여넣기 하는 것 만으로 쉽게 경제 용어를 정리해서 알려주는 챗봇입니다.

- 왜 이코파인더를 기획하게 되었나요?
    - 경제를 막 공부하기 시작한 초심자들은 경제 공부를 하려고 뉴스를 키지만 이해할수 없는 어려운 용어들로 경제에 입문하기도 전 큰 장벽에 가로막히고 맙니다.
      더불어, 공부를 한다고 하더라도, 경제 용어를 하나하나 검색하는 과정에서 불필요한 시간이 너무 많이 소요됩니다.
      이런 불편함을 줄이기 위해 경제 용어를 자동으로 정리해주는 서비스를 기획했습니다.

- 주요 기능
  - 사용자가 제공하는 경제 뉴스 링크를 통해 해당 뉴스 내용을 자동으로 크롤링 해줍니다.
  - 기사 내에서 등장하는 경제 용어들을 자동으로 추출 해줍니다.
  - 경제 용어에 대한 간단한 정의와 설명을 통해 독자가 뉴스 내용을 더 쉽게 이해하고, 경제에 대한 지식을 향상시킬 수 있도록 돕습니다.
&nbsp;
&nbsp; 
## 멤버 소개

|김예훈|최현용|이연규|박도아|
|------|---|---|---|
|![image](https://github.com/user-attachments/assets/bfa3a16a-6af9-4fd3-a146-9d02b1fd65d7)|![image](https://github.com/user-attachments/assets/9d1e513d-4889-4b82-af14-4d3a7f07ca7c)|![image](https://github.com/user-attachments/assets/51227f7a-99e8-4b9a-bac6-f4d4062289ca)|![image](https://github.com/user-attachments/assets/cb690d63-42f1-45d7-ba70-afa11e756e5b)|
|@yehoon-already-have|@gusdyddl1212|@Da-413|@parkdoa|


&nbsp; 
&nbsp; 
## 이코파인더 사용법 및 기능
1. 정보 제공을 원하는 뉴스의 url 또는 기사 텍스트를 입력창에 입력합니다.
&nbsp;

![ecofinder-step1-gif](https://github.com/user-attachments/assets/2f0e67d9-9dce-438d-8f22-e98ffb3b2a18)

2. 답변으로 뉴스에 포함된 경제 용어의 해설과 뉴스 내용을 동시에 제공받습니다. (약 20 ~ 30초 소요)
&nbsp;

![ecofinder-step2-gif](https://github.com/user-attachments/assets/eacd9050-ee12-4b4b-8f68-05c6a9257272)

3. 경제와 관련 없는 기사의 경우 경제 관련 용어가 없다는 답변을 받습니다.
&nbsp;

![ecofinder-step3-gif](https://github.com/user-attachments/assets/98103686-6d61-453b-bc9f-245d2c7da96f)


&nbsp; 
&nbsp; 
## 로컬 실행 방법
- FrontEnd
    - frontend 폴더에 접근하고 아래 코드를 실행합니다.
      ```
      npm start
      ```
    - localhost:1234에 접속합니다.
- BackEnd
    - backend 폴더 접근하고 라이브러리 설치를 위해 아래 코드를 실행합니다.
      ```
      python -m pip install -r requirements.txt
      ```
    - 백엔드 실행을 위해 아래 코드를 실행합니다.
      ```
      python app.py
      ```
