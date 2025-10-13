# test_analyzer.py

# 테스트하고 싶은 함수를 qr_analyzer.py 파일에서 불러옵니다.
from qr_analyzer import extract_url_from_image

# --- 테스트 설정 ---
# 여기에 테스트하고 싶은 이미지 파일의 이름을 넣으세요.
# 이 파일은 test_analyzer.py와 같은 폴더에 있어야 합니다.
TEST_IMAGE_FILE = "3rd_orbit__qr.png"
# TEST_IMAGE_FILE = "test_qr.png" # 다른 파일로 바꿔가며 테스트 해보세요.

print(f"--- 🧪 '{TEST_IMAGE_FILE}' 파일 테스트 시작 ---")

try:
    # 파일을 '바이너리 읽기' 모드('rb')로 엽니다.
    # 이것이 웹 서버가 파일을 처리하는 방식과 가장 유사합니다.
    with open(TEST_IMAGE_FILE, 'rb') as image_file:

        # 함수를 호출하고 결과를 받습니다.
        result_url = extract_url_from_image(image_file)

        # 결과에 따라 다른 메시지를 출력합니다.
        if result_url:
            print(f"✅ 성공! 추출된 URL: {result_url}")
        else:
            print("⚠️ 실패! QR 코드를 찾지 못했거나 파일에 문제가 있습니다.")

except FileNotFoundError:
    print(f"❌ 오류! '{TEST_IMAGE_FILE}' 파일을 찾을 수 없습니다.")

print("--- 테스트 종료 ---")