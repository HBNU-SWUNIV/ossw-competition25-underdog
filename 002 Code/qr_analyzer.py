# qr_analyzer.py
from PIL import Image
import zxingcpp

def extract_url_from_image(image_file):
    """
    zxing-cpp 라이브러리를 사용하여 QR 코드에서 URL을 추출합니다.
    성공시 URL 문자열, 실패시 None을 반환합니다.
    """
    try:
        image = Image.open(image_file)
        results = zxingcpp.read_barcodes(image)

        if results:
            qr_data = results[0].text
            print(f"✅ QR 코드 탐지 성공: {qr_data}")
            return qr_data  # 문자열 직접 반환
        else:
            print("⚠️ 이미지는 정상이지만 QR 코드를 찾지 못했습니다.")
            return None

    except Exception as e:
        print(f"❌ 이미지 파일 처리 중 오류 발생: {e}")
        return None