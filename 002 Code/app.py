# app.py (최종 완성본)

import os
from flask import Flask, render_template, request, jsonify # jsonify를 꼭 import 해야 합니다.
from werkzeug.utils import secure_filename
# 우리 팀의 핵심 모듈들을 불러옵니다.
from qr_analyzer import extract_url_from_image
from safe_url import check_url_safety

# --- Flask 앱 생성 및 기본 설정 ---
app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- 페이지 라우팅 ---
@app.route('/')
def index():
    return render_template('index.html')

# --- 파일 업로드 및 분석 API (가장 중요한 부분) ---
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
            return jsonify({'status': '오류', 'url': 'N/A', 'reason': '이미지에서 QR 코드를 찾을 수 없거나 손상된 파일입니다.'})
        
        # 2. 업그레이드된 safe_url 함수를 호출하고 결과(딕셔너리)를 받습니다.
        safety_info = check_url_safety(url)

        # 3. 결과에 따라 최종 상태(status)와 설명(reason)을 결정합니다.
        final_status = safety_info['status']
        reason = "알려진 위협이 없는 안전한 URL입니다."

        # 리디렉션이 있었고, 최종 목적지가 '안전'한 경우에만 '주의' 상태로 변경
        if safety_info['redirected'] and final_status == "안전":
            final_status = "주의"
            reason = "이 QR코드는 다른 주소로 이동합니다. 최종 목적지는 안전해 보입니다."
        elif final_status == "위험":
            reason = "알려진 피싱 또는 악성 사이트입니다."
        elif final_status == "오류":
             reason = "URL의 안전성을 검사하는 중 오류가 발생했습니다."

        # 4. 프론트엔드에 보낼 최종 결과(JSON)를 만듭니다.
        result = {
            'status': final_status,
            # 리디렉션이 있었다면 최종 목적지를, 아니면 원본 URL을 보여줍니다.
            'url': safety_info['final_url'] if safety_info['redirected'] else safety_info['original_url'],
            'reason': reason
        }
        
        # 5. 최종 결과를 JSON 형태로 프론트엔드에 전송
        return jsonify(result)

# --- 서버 실행 ---
if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)