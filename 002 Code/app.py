import os 
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from qr_analyzer import extract_url_from_image

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

# 3. 파일 업로드 처리
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'status': '오류', 'reason': '요청에 파일이 없습니다.'}), 400
    
    file = request.files['file']

    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({'status': '오류', 'reason': '파일을 선택하지 않았거나, 허용되지 않는 파일 형식입니다.'}), 400
    
    if file:
        # [수정] 파일을 저장하는 대신, 메모리에서 바로 함수에 전달합니다!
        # filename = secure_filename(file.filename)
        # filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        # file.save(filepath)
        
        # [수정] 새로 import한 함수를 사용합니다.
        result_url = extract_url_from_image(file)

        # QR 코드를 찾지 못했을 경우의 처리
        if result_url is None:
            return jsonify({'status': '오류', 'url': 'N/A', 'reason': '이미지에서 QR 코드를 찾을 수 없습니다.'})
        
        # (이후 URL 안전성 검사 로직은 여기에 추가하면 됩니다.)
        # ...

        # 분석 결과를 웹페이지에 표시 (이 부분은 나중에 JSON으로 바꿀 예정)
        return f"""
            <h1>QR 코드 분석 완료</h1>
            <p><strong>추출된 데이터:</strong> {result_url}</p>
            <a href="/">다른 이미지로 다시 검사하기</a>
        """
# 4. 서버 실행
if __name__ == '__main__':
    # 'uploads' 폴더가 없으면 자동으로 생성
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True) # 개발용 서버 실행
