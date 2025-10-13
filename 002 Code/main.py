from pyzbar.pyzbar import decode
from PIL import Image


# 기존 코드를 함수로 감싸고, 이미지 경로를 인자로 받도록 수정
def analyze_qr_code(image_path):
    """
    이미지 파일 경로를 받아 QR 코드를 분석하고,
    추출된 데이터를 문자열로 반환합니다.
    """
    try:
        img = Image.open(image_path)
        result = decode(img)

        if result:
            # QR 코드를 찾으면 첫 번째 결과의 데이터를 디코딩하여 반환
            qr_data = result[0].data.decode('utf-8')
            return qr_data
        else:
            # 이미지에서 QR 코드를 못 찾은 경우
            return "QR 코드를 찾을 수 없습니다."
    except Exception as e:
        # 파일 오류 등 예외 처리
        return f"분석 중 오류 발생: {e}"

# 아래 부분은 단독 실행 시 테스트를 위한 코드로 남겨둘 수 있습니다.
# if __name__ == '__main__':
#     # 'test_qr.png' 파일로 함수가 잘 동작하는지 테스트
#     decoded_data = analyze_qr_code('test_qr.png')
#     print(f"테스트 결과: {decoded_data}")