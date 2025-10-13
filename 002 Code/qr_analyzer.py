from pyzbar.pyzbar import decode
from PIL import Image
from safe_url import check_url_safety


def analyze_qr_code(image_path):
    """
    이미지 파일 경로를 받아 QR 코드를 분석하고,
    추출된 데이터를 문자열(URL)로 반환합니다.
    """
    try:
        img = Image.open(image_path)
        result = decode(img)

        if result:
            qr_data = result[0].data.decode('utf-8')
            return qr_data
        else:
            return None  # QR 코드가 없을 경우
    except Exception as e:
        print(f"❌ 이미지 분석 중 오류 발생: {e}")
        return None


if __name__ == "__main__":
    print("🔍 QR 코드 기반 URL 안전성 검사 프로그램 시작")

    # 1️⃣ 이미지 파일 경로 입력받기
    image_path = input("분석할 QR 이미지 파일 경로를 입력하세요 (예: test.png): ").strip()

    # 2️⃣ QR 코드 분석
    qr_data = analyze_qr_code(image_path)

    if qr_data is None:
        print("⚠️ 이미지에서 QR 코드를 찾을 수 없습니다.")
    else:
        print(f"📦 QR 코드에서 추출된 데이터: {qr_data}")

        # 3️⃣ URL 안전성 검사
        result = check_url_safety(qr_data)
        print(f"✅ 검사 결과: {result}")
