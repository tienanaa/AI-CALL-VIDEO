from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware 
from deepface import DeepFace 
import shutil 
import uuid # Dùng để tạo tên file duy nhất
import os
import asyncio # Dùng để chạy DeepFace ở luồng phụ

# Import router từ file api/room.py
from api.room import router as room_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ĐĂNG KÝ ROUTER
app.include_router(room_router, prefix="/api")

@app.get("/")
async def read():   
    return {"message":"Server video call AI đang chạy"}

@app.post("/predict")
async def create_upload_file(file: UploadFile = File(...)):
    # 1. Tạo tên file duy nhất cho mỗi request
    unique_id = str(uuid.uuid4())
    file_path = f"temp_{unique_id}.jpg"

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 2. Đưa tác vụ AI nặng sang một luồng khác (thread) để không làm lag Video Call
        ket_qua = await asyncio.to_thread(DeepFace.analyze, img_path=file_path, actions=['emotion'])
        emotion = ket_qua[0]['dominant_emotion']

        return {
            'status': 'success',
            'emotion': emotion,
            'confidence': 0.95
        }
    except Exception as e: 
        print(f"Lỗi: {e}")
        return {"status": "error", "emotion": "No Face", "confidence": 0}
    finally:
        # 3.  xóa ảnh sau khi phân tích xong để tránh rác ổ cứng
        if os.path.exists(file_path):
            os.remove(file_path)