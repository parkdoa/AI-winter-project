import os
import time
import re
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from langchain.chains import RetrievalQA
from langchain_pinecone import PineconeVectorStore
from langchain_upstage import ChatUpstage, UpstageEmbeddings
from pinecone import Pinecone, ServerlessSpec
from pydantic import BaseModel
import validators  # URL 유효성 검사를 위한 라이브러리

# 환경 변수 로드
from dotenv import load_dotenv
load_dotenv()

# Upstage 모델들
chat_upstage = ChatUpstage()
embedding_upstage = UpstageEmbeddings(model="embedding-query")

pinecone_api_key = os.environ.get("PINECONE_API_KEY")
pc = Pinecone(api_key=pinecone_api_key)
index_name = "economy-data-2"

# Pinecone 인덱스 생성
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=4096,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )

pinecone_vectorstore = PineconeVectorStore(index=pc.Index(index_name), embedding=embedding_upstage)
pinecone_retriever = pinecone_vectorstore.as_retriever(
    search_type='mmr',  # default : similarity / mmr 알고리즘
    search_kwargs={"k": 3}  # 검색 시 상위 3개의 관련 문서
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic 모델 정의
class MessageRequest(BaseModel):
    message: str

# Selenium 설정
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Chrome 옵션 설정 (헤드리스 모드)
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("window-size=1920,1080")

# ChromeDriver 자동 설치 및 실행
service = Service(ChromeDriverManager().install())

# Selenium을 이용한 기사 크롤링 함수
def scrape_article_content(article_link: str) -> str:
    # URL 유효성 검사
    if not validators.url(article_link):
        raise ValueError(f"잘못된 URL입니다: {article_link}")

    try:
        # 기사 페이지로 이동
        driver = webdriver.Chrome(service=service, options=options)

        driver.get(article_link)
        time.sleep(3)  # 페이지 로딩 대기

        # 기사 본문 내용 가져오기 (CSS Selector 사용)
        paragraphs = driver.find_elements(By.CSS_SELECTOR, "#dic_area")
        if not paragraphs:
            raise ValueError(f"기사 본문을 찾을 수 없습니다: {article_link}")
        
        # Preserve original formatting
        content = paragraphs[0].get_attribute('innerHTML')
        # Convert HTML line breaks to newlines
        content = content.replace('<br>', '\n').replace('</br>', '\n')
        # Strip remaining HTML tags
        content = re.sub('<[^<]+?>', '', content)
        # Normalize newlines
        content = re.sub(r'\n\s*\n', '\n\n', content)
        
        return content.strip()
    except Exception as e:
        raise ValueError(f"기사 크롤링 중 오류 발생: {e}")
    finally:
        driver.quit()

# 경제 용어를 찾는 엔드포인트
@app.post("/findword")
async def findword_endpoint(req: MessageRequest):
    try:
        article_link = req.message
        article_content = ""

        if validators.url(article_link):
            # URL을 통해 기사 내용 크롤링
            article_content = scrape_article_content(article_link)
            user_message = article_content
        else:
            # 텍스트가 제공되면 바로 사용
            user_message = req.message
            article_content = user_message

        findword_message = f"""
너는 아래 기사에서 경제 용어를 찾아서 리스트업 해줘
{user_message}

위 단어들 중 경제 용어가 없다면 "경제 관련 단어가 없습니다"라고 말말하고 아래 내용은 건너 뛰어
만약에 경제 용어가 있다면 경제 관련 단어만 추출해서 무슨 뜻인지 번호를 매겨서 아래와 같은 형식으로 나열해줘 그 외 아무말 하지마.

예시 ) 1. 국내총투자율 : 국내 총투자율(gross domestic investment ratio)은 국민경제가 구매한 재화 중에서 
자산의 증가로 나타난 부분이 국민총처분가능소득에서 차지하는 비율을 의미한다.
"""

        qa = RetrievalQA.from_chain_type(
            llm=chat_upstage,
            chain_type="map_reduce",
            retriever=pinecone_retriever,
            return_source_documents=True
        )

        result = qa(findword_message)

        has_economic_terms = "경제 관련 단어가 없" not in result['result']
        
        print(result['result'])
        print(article_content)
        # Return the result with article_content only if economic terms were found
        return {
            "reply": result['result'],
            "article_content": article_content if has_economic_terms else ""
        }

    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))

# Health check 엔드포인트


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
