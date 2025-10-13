import os 
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import main

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
    # 사용자가 올린 파일 가져오기
    if 'file' not in request.files:
        return "요청에 파일이 없습니다."
    file = request.files['file']

    if file.filename == '' or not allowed_file(file.filename):
        return "파일을 선택하지 않았거나, 허용되지 않는 파일 형식입니다. (png, jpg, jpeg만 가능)"
    
    if file:
        # 안전한 파일 이름으로 변경 (해킹방지)
        filename = secure_filename(file.filename)
        # 파일을 서버의 'uploads/' 폴더에 저장
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        # 저장된 이미지 파일 경로를 main.py의 함수에 대입!
        result_url = main.analyze_qr_code(filepath)

         # 분석 결과를 웹페이지에 표시
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
