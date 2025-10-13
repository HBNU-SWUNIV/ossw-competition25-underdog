# qr_analyzer.py

from PIL import Image
import zxingcpp

def extract_url_from_image(image_file: str):
    """
    zxing-cpp 라이브러리를 사용하여 QR 코드를 추출하고,
    성공/실패 여부와 상세 내용을 딕셔너리로 반환합니다.
    """
    try:
        # 1. Pillow를 사용해 이미지를 엽니다.
        #    이 단계에서 파일이 깨졌거나 지원하지 않는 형식이면 예외가 발생합니다.
        image = Image.open(image_file)
        
        # 2. zxing-cpp로 QR 코드를 찾습니다.
        results = zxingcpp.read_barcodes(image)

        if results:
            # ✅ 성공: 상태와 데이터를 함께 반환
            qr_data = results[0].text
            ## 여기 바꿈 + 왜바꿧냐? 이유섭 프론트엔드에서 결과값까지 다 출력해버려서
            # 너 qr 결과값이랑 이유섭 프론트엔드 출력값이 겹쳐서 결과값이 안나오고 자꾸튕겨서
            print(f"✅ QR 코드 탐지 성공: {qr_data}")
            return {
                "status": "success",
                "data": qr_data
            }
        else:
            # ⚠️ 실패 1: 이미지는 정상이지만 QR 코드를 찾지 못함
            print("⚠️ 이미지는 정상이지만 QR 코드를 찾지 못했습니다.")
            return {
                "status": "error",
                "message": "QR code not found in the image."
            }
            ##여기 위에도

    except Exception as e:
        # ❌ 실패 2: 파일 처리 중 예상치 못한 오류 발생 (가장 중요한 부분!)
        # 예를 들어, 파일이 실제 이미지가 아니거나 심하게 손상된 경우 여기에 해당됩니다.
        print(f"❌ 이미지 파일 처리 중 오류 발생: {e}")
        return {
            "status": "error",
            "message": f"An unexpected error occurred while processing the image: {str(e)}"
        }
    ##여기도요