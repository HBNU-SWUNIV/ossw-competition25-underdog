# safe_url.py

import os
import requests
import json
from dotenv import load_dotenv  # .env 파일에서 API 키 읽기

# 1️ .env 파일에서 GOOGLE_API_KEY 읽어오기
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

def check_url_safety(url_to_check):
    """
    Google Safe Browsing API를 이용해 URL의 안전성을 검사하고
    '안전' 또는 '위험' 중 하나를 반환합니다.
    """
    # API 요청에 필요한 JSON 형식
    request_body = {
        "client": {
            "clientId": "QR-Safety-Scanner",
            "clientVersion": "1.0"
        },
        "threatInfo": {
            "threatTypes": [
                "MALWARE",
                "SOCIAL_ENGINEERING",
                "UNWANTED_SOFTWARE"
            ],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": url_to_check}]
        }
    }

    # Google Safe Browsing API 호출
    response = requests.post(
        f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={API_KEY}",
        data=json.dumps(request_body)
    )

    # 응답 확인
    if response.status_code != 200:
        return f"API 요청 실패: {response.status_code} ({response.text})"

    result = response.json()

    if result == {}:
        return "안전"
    else:
        return "위험"

# 3️ 단독 실행 시 테스트용
if __name__ == "__main__":
    test_safe = "https://www.google.com"
    test_danger = "http://malware.testing.google.test/testing/malware/"
    print(f"{test_safe} 검사 결과: {check_url_safety(test_safe)}")
    print(f"{test_danger} 검사 결과: {check_url_safety(test_danger)}")
