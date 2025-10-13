import cv2
import numpy as np
from PIL import Image # Pillow 라이브러리가 필요합니다.

def extract_url_from_image(image_file):
    """
    OpenCV를 사용해 이미지 파일에서 QR코드 속 URL을 추출합니다.
    파일이 손상되었거나 이미지가 아닌 경우 등 예외 상황을 처리합니다.
    """
    try:
        # 1. Pillow를 사용해 메모리에서 이미지를 엽니다.
        #    이 단계에서 파일이 깨졌거나 지원하지 않는 형식이면 예외가 발생합니다.
        pil_image = Image.open(image_file)

        # 2. 이미지를 OpenCV가 처리할 수 있는 NumPy 배열 형태로 변환합니다.
        image = np.array(pil_image)

        # 3. 컬러 이미지를 흑백으로 변환합니다. (핵심 안정성 강화)
        #    - 투명도(Alpha) 채널이 포함된 PNG 파일(4채널)은 BGR(3채널)로 먼저 변환합니다.
        #    - 이 과정을 거치지 않으면 cvtColor 함수에서 오류가 발생할 수 있습니다.
        if len(image.shape) == 3 and image.shape[2] == 4:
            image = cv2.cvtColor(image, cv2.COLOR_RGBA2BGR)
        
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # 4. OpenCV의 QR 코드 탐지기 생성 및 실행
        detector = cv2.QRCodeDetector()
        data, points, straight_qrcode = detector.detectAndDecode(gray_image)

        if data:
            return data  # 성공적으로 URL을 찾은 경우
        else:
            return None  # 이미지는 정상이지만 QR 코드를 못 찾은 경우

    except Exception as e:
        # Image.open()에서 오류가 발생했거나, 이미지 변환 중 오류가 발생한 경우
        print(f"❌ 이미지 파일 처리 중 오류 발생: {e}")
        return None # 서버에 문제가 있었음을 알리기 위해 None 반환