from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import shutil
import os
from pathlib import Path
from datetime import datetime
import uuid
from qr_analyzer import extract_url_from_image
from fastapi.middleware.cors import CORSMiddleware


# FastAPI 앱 생성
app = FastAPI(title="Image Upload Server")

# ▼▼▼▼▼▼ 이 부분을 추가하세요 ▼▼▼▼▼▼
origins = [
    "http://localhost",
    "http://localhost:5500",
    "http://127.0.0.1",
    "http://127.0.0.1:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # 모든 메소드 허용
    allow_headers=["*"], # 모든 헤더 허용
)
   
# 업로드 폴더 설정
UPLOAD_FOLDER = "uploads"
Path(UPLOAD_FOLDER).mkdir(exist_ok=True)

# 허용된 이미지 확장자
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"}

# 최대 파일 크기 (10MB)
MAX_FILE_SIZE = 10 * 1024 * 1024


def is_allowed_file(filename: str) -> bool:
    """파일 확장자 검증"""
    return Path(filename).suffix.lower() in ALLOWED_EXTENSIONS


def generate_unique_filename(original_filename: str) -> str:
    """고유한 파일명 생성 (타임스탬프 + UUID)"""
    ext = Path(original_filename).suffix
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid.uuid4())[:8]
    return f"{timestamp}_{unique_id}{ext}"


def process_image(file_path: str):
    """
    qr_analyzer.py의 함수를 호출하여 이미지를 처리합니다.
    """
    print(f"Analyzing image with qr_analyzer: {file_path}")
    
    # 호출하는 함수 이름도 똑같이 바꿔주세요!
    result = extract_url_from_image(file_path)
    return result


@app.get("/")
async def root():
    """서버 상태 확인"""
    return {"message": "Image Upload Server is running", "status": "OK"}


@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    """이미지 파일 업로드 엔드포인트"""
    
    # 1. 파일이 있는지 확인
    if not file:
        raise HTTPException(status_code=400, detail="No file provided")
    
    # 2. 파일 확장자 검증
    if not is_allowed_file(file.filename):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # 3. 파일 크기 확인
    file.file.seek(0, 2)  # 파일 끝으로 이동
    file_size = file.file.tell()  # 파일 크기 확인
    file.file.seek(0)  # 다시 처음으로
    
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Max size: {MAX_FILE_SIZE / 1024 / 1024}MB"
        )
    
    # 4. 고유한 파일명 생성
    unique_filename = generate_unique_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
    
    try:
        # 5. 파일 저장
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # 6. 이미지 처리 함수 호출
        processing_result = process_image(file_path)
        
        # 7. 성공 응답
        return JSONResponse(
            status_code=200,
            content={
                "message": "File uploaded successfully",
                "original_filename": file.filename,
                "saved_filename": unique_filename,
                "file_path": file_path,
                "file_size": file_size,
                "processing_result": processing_result
            }
        )
    
    except Exception as e:
        # 에러 발생 시 파일 삭제
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@app.get("/uploads/{filename}")
async def get_uploaded_file(filename: str):
    """업로드된 파일 정보 조회"""
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    file_size = os.path.getsize(file_path)
    return {
        "filename": filename,
        "path": file_path,
        "size": file_size,
        "exists": True
    }


@app.delete("/uploads/{filename}")
async def delete_uploaded_file(filename: str):
    """업로드된 파일 삭제"""
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    try:
        os.remove(file_path)
        return {"message": "File deleted successfully", "filename": filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Delete failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)