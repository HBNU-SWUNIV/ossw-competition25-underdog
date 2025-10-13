# qr_analyzer.py (zxing-cpp 최종 엔진)

from PIL import Image
import zxingcpp

def extract_url_from_image(image_file):
    """
    가장 강력한 zxing-cpp 라이브러리를 사용하여 QR 코드를 추출합니다.
    복잡한 디자이너 QR 코드에 대한 인식률이 매우 높습니다.
    """
    try:
        # 1. Pillow를 사용해 이미지를 엽니다.
        image = Image.open(image_file)
        
        # 2. zxing-cpp의 read_barcodes 함수로 QR 코드를 찾습니다.
        results = zxingcpp.read_barcodes(image)

        # 3. QR 코드를 찾았는지 확인합니다.
        if results:
            # 첫 번째로 찾은 QR 코드의 텍스트를 반환합니다.
            return results[0].text
        else:
            return None # QR 코드를 못 찾은 경우

    except Exception as e:
        print(f"❌ 이미지 파일 처리 중 예상치 못한 오류 발생: {e}")
        return None