from fastapi.testclient import TestClient
from app import app  # FastAPI 애플리케이션

client = TestClient(app)

def test_findword_with_valid_url():
    # 테스트용 URL
    test_url = "https://n.news.naver.com/mnews/article/016/0002410477"
    
    # 메시지 전송
    response = client.post("/findword", json={"message": test_url})

    # 응답 상태 코드 확인
    assert response.status_code == 200

    # 응답 내용 확인
    data = response.json()
    assert "reply" in data
    assert isinstance(data["reply"], str)  # reply가 문자열인지 확인

def test_findword_with_text_message():
    # 테스트용 텍스트 메시지
    test_message = "MSCI 신흥국 지수에서 한국 비중이 줄어든 것은 코스피가 지난해 연간 기준 9.63% 하락한 영향 때문으로 분석된다."
    
    # 메시지 전송
    response = client.post("/findword", json={"message": test_message})

    # 응답 상태 코드 확인
    assert response.status_code == 200

    # 응답 내용 확인
    data = response.json()
    assert "reply" in data
    assert isinstance(data["reply"], str)  # reply가 문자열인지 확인

def test_findword_without_economic_terms():
    # 경제 용어가 없는 텍스트 메시지
    test_message = "천마가 짜장을 만나 일냈네! 사각사각 씹히는 별미"
    
    # 메시지 전송
    response = client.post("/findword", json={"message": test_message})

    # 응답 상태 코드 확인
    assert response.status_code == 200

    # 응답 내용 확인
    data = response.json()
    assert "경제 관련 단어가 없습니다" in data["reply"]  # 경제 용어가 없다는 메시지가 포함되어야 함
