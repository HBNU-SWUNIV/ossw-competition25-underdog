# safe_url.py (API 중심 최종 버전)

import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def check_url_safety(url_to_check):
    final_url = url_to_check
    redirected = False
    
    # 1. URL 추적 (더 안정적인 GET 방식으로 변경)
    try:
        # stream=True로 헤더만 먼저 받고, 전체 페이지를 다운로드하지 않아 빠릅니다.
        with requests.get(url_to_check, allow_redirects=True, timeout=5, verify=False, stream=True) as response:
            final_url = response.url
        
        if url_to_check != final_url:
            redirected = True

    except requests.exceptions.RequestException as e:
        print(f"❌ URL 추적 중 오류 발생: {e}")
        # 추적 실패 시, 바로 '오류' 상태 반환
        return {
            "original_url": url_to_check, "final_url": final_url,
            "redirected": False, "status": "오류",
            "reason": "URL에 접속할 수 없습니다. (네트워크 오류)"
        }

    # 2. Google Safe Browsing API 검사
    # (API 키가 없으면 바로 오류 반환)
    if not API_KEY:
        return {
            "original_url": url_to_check, "final_url": final_url,
            "redirected": redirected, "status": "오류",
            "reason": "서버에 API 키가 설정되지 않았습니다."
        }
        
    request_body = {
        "client": {"clientId": "QR-Safety-Scanner", "clientVersion": "1.0"},
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": final_url}] 
        }
    }

    safety_status = "안전"
    try:
        google_response = requests.post(
            f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={API_KEY}",
            json=request_body,
            timeout=5
        )
        if google_response.status_code == 200:
            if google_response.json().get('matches', []): 
                safety_status = "위험"
        else:
            safety_status = "오류" 
            print(f"API 요청 실패: {google_response.status_code} - {google_response.text}")

    except requests.exceptions.RequestException as e:
        safety_status = "오류"
        print(f"Google API 연결 오류: {e}")
    
    return {
        "original_url": url_to_check,
        "final_url": final_url,
        "redirected": redirected,
        "status": safety_status
    }