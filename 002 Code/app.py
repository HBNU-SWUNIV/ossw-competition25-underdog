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

@app.route('/scan', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'status': '오류', 'reason': '요청에 파일이 없습니다.'}), 400
    
    file = request.files['file']

    if file.filename == '':
        return jsonify({'status': '오류', 'reason': '파일을 선택하지 않았습니다.'}), 400
    
    if file and allowed_file(file.filename):
        url = extract_url_from_image(file)

        if url is None:
            return jsonify({'status': '오류', 'url': 'N/A', 'reason': '이미지에서 QR 코드를 찾을 수 없거나 손상된 파일입니다.'})
        
        safety_info = check_url_safety(url)

        # --- ✨ 여기가 최종 판단 로직! ✨ ---
        final_status = safety_info['status']
        reason = ""
        
        if final_status == "위험":
            reason = "Google Safe Browsing에서 최종 목적지를 위험 사이트로 분류했습니다."
        elif final_status == "오류":
            reason = safety_info.get('reason', "URL의 안전성을 검사하는 중 오류가 발생했습니다.")
        elif final_status == "안전":
            shortener_domains = ["q.me-qr.com", "bit.ly", "tinyurl.com", "goo.gl", "me2.do"]
            original_domain = ""
            try:
                original_domain = safety_info['original_url'].split('/')[2]
            except (IndexError, AttributeError):
                pass

            if safety_info['redirected'] and original_domain in shortener_domains:
                final_status = "주의"
                reason = "단축 URL이 사용되었습니다. 최종 목적지는 안전해 보이지만 주의가 필요합니다."
            else:
                final_status = "안전"
                reason = "알려진 위협이 없는 안전한 URL입니다."
        # -----------------------------------
        
        # --- ✨ 여기가 Key 이름 통일 부분! ✨ ---
        result = {
            'status': final_status,
            'url': safety_info['final_url'],  # 'final_url' 대신 'url' 키를 사용
            'reason': reason
        }
        # -----------------------------------

        return jsonify(result)

# --- 서버 실행 ---
if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)