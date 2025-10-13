import os 
from flask import Flask, render_template, request, jsonify #jsonify 추가
from werkzeug.utils import secure_filename
from qr_analyzer import extract_url_from_image
from safe_url import check_url_safety # safe_url 추가

# 1. flask 앱 생성

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads' #업로드 파일 저장 폴더
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    #업로드 파일 확장자 확인 함수
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 2. 메인 페이지
@app.route('/')
def index():
    # templates 폴더의 index.html 파일을 사용자에게 보여줌
    return render_template('index.html')

# 3. 파일 업로드 처리(전체수정)
@app.route('/scan', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'status': '오류', 'reason': '요청에 파일이 없습니다.'}), 400
    
    file = request.files['file']

    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({'status': '오류', 'reason': '파일을 선택하지 않았거나, 허용되지 않는 파일 형식입니다.'}), 400
    
    if file:
        # 1. QR 코드에서 URL 추출
        url = extract_url_from_image(file)

        if url is None:
            return jsonify({'status': '오류', 'url': 'N/A', 'reason': '이미지에서 QR 코드를 찾을 수 없습니다.'})
        
        # 2. URL 안전성 검사
        safety_status_from_api = check_url_safety(url)

        # 3. 프론트엔드에 보낼 최종 결과 만들기
        if "bit.ly" in url or "me2.do" in url:
            final_status = "주의"
            reason = "단축 URL이 사용되었습니다. 최종 목적지를 반드시 확인하세요."
        elif safety_status_from_api == "위험":
            final_status = "위험"
            reason = "알려진 피싱 또는 악성 사이트입니다."
        else:
            final_status = "안전"
            reason = "알려진 위협이 없는 안전한 URL입니다."
        
        result = {
            'status': final_status,
            'url': url,
            'reason': reason
        }
        
        # 4. 최종 결과를 JSON 형태로 프론트엔드에 전송
        return jsonify(result)

# 4. 서버 실행
if __name__ == '__main__':
    # 'uploads' 폴더가 없으면 자동으로 생성
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True) # 개발용 서버 실행
