# safe_url.py (리디렉션 추적 기능 추가)

import os
import requests
import json
from dotenv import load_dotenv

# .env 파일에서 GOOGLE_API_KEY 읽어오기
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

def check_url_safety(url_to_check):
    """
    URL 리디렉션을 추적하여 최종 목적지 주소를 알아낸 뒤,
    그 최종 주소의 안전성을 검사하고 상세 정보를 반환합니다.
    """
    final_url = url_to_check
    redirected = False

    try:
        # 1. HEAD 요청을 보내 리디렉션이 있는지 빠르게 확인합니다.
        # allow_redirects=True 옵션이 자동으로 최종 목적지까지 따라가게 해줍니다.
        # timeout=5는 응답이 너무 길어지는 것을 방지합니다.
        response = requests.head(url_to_check, allow_redirects=True, timeout=5)
        
        # 2. 최종 도착한 URL을 확인합니다.
        final_url = response.url

        # 3. 원래 URL과 최종 URL이 다르면, 리디렉션이 발생한 것입니다.
        if url_to_check != final_url:
            redirected = True

    except requests.RequestException as e:
        print(f"URL 추적 중 오류 발생: {e}")
        # 네트워크 오류 발생 시, 일단 원본 URL로 검사를 시도하고 리디렉션 여부는 알 수 없음(False)으로 둡니다.
        pass

    # 4. '최종 목적지 URL'로 Google API 검사를 수행합니다.
    request_body = {
        "client": {
            "clientId": "QR-Safety-Scanner",
            "clientVersion": "1.0"
        },
        "threatInfo": {
            "threatTypes": [
                "MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE",
                "POTENTIALLY_HARMFUL_APPLICATION"
            ],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": final_url}] # final_url을 검사!
        }
    }

    safety_status = "안전"
    try:
        google_response = requests.post(
            f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={API_KEY}",
            data=json.dumps(request_body),
            timeout=5
        )
        if google_response.json() != {}:
            safety_status = "위험"
    except requests.RequestException as e:
        print(f"Google API 요청 중 오류 발생: {e}")
        safety_status = "오류" # API 통신 실패 시 '오류' 상태 반환

    
    # 5. 서버(app.py)에서 판단할 수 있도록 모든 정보를 딕셔너리 형태로 반환합니다.
    return {
        "original_url": url_to_check,
        "final_url": final_url,
        "redirected": redirected,
        "status": safety_status
    }

# --- 단독 실행 시 테스트용 ---
if __name__ == "__main__":
    # 테스트용 URL 목록
    test_urls = {
        "안전한 주소": "https://www.google.com",
        "위험한 주소": "http://malware.testing.google.test/testing/malware/",
        "리디렉션 주소 (단축 URL 예시)": "https://bit.ly/3x0x0x0" # 실제 작동하는 단축 URL로 테스트하면 더 좋습니다.
    }

    for name, url in test_urls.items():
        result_info = check_url_safety(url)
        print(f"\n--- {name} ({url}) 검사 ---")
        print(f"최종 목적지: {result_info['final_url']}")
        print(f"리디렉션 발생: {'예' if result_info['redirected'] else '아니오'}")
        print(f"구글 API 검사 결과: {result_info['status']}")