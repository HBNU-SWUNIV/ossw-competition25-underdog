# qr_analyzer.py (최종 수정본)

import cv2
import numpy as np
from PIL import Image # Pillow 라이브러리가 필요합니다.

def extract_url_from_image(image_file):
    """
    업로드된 이미지 파일(실물)을 직접 받아서 QR코드 속 URL을 추출합니다.
    URL을 찾으면 URL 문자열을, 못 찾으면 None을 반환합니다.
    """
    try:
        # 1. Pillow를 사용해 메모리에서 이미지를 읽어옵니다.
        pil_image = Image.open(image_file)
        # 2. 이미지를 OpenCV가 처리할 수 있는 NumPy 배열 형태로 변환합니다.
        image = np.array(pil_image)
        # 컬러 이미지를 흑백으로 변환하여 인식률을 높입니다.
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # 3. OpenCV의 QR 코드 탐지기 생성 및 실행 (이 부분은 동일)
        detector = cv2.QRCodeDetector()
        data, points, straight_qrcode = detector.detectAndDecode(gray_image)

        if data:
            return data
        else:
            return None

    except Exception as e:
        print(f"이미지 처리 중 오류 발생: {e}")
        return None