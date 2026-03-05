from fastapi import FastAPI,File, UploadFile,WebSocket
from fastapi.middleware.cors import CORSMiddleware  # cap quyen
from deepface import DeepFace # AI phan tich cam xuc
import shutil #xu ly du lieu anh

app= FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def read():
    return {"message":"Server video call AI đang chạy"}

@app.post("/predict")
async def create_upload_file(file: UploadFile = File(...)):
   
    print(f"Đã nhận file ảnh: {file.filename}")

    file_path="temp.jpg"

    #luu du lieu len o cung => co dia chi cu the
    with open(file_path,"wb") as buffer:
        shutil.copyfileobj(file.file,buffer)

    try:
        ket_qua=DeepFace.analyze(img_path=file_path, actions=['emotion'])
        emotion=ket_qua[0]['dominant_emotion']

        print(f'emotion: {emotion}')
        return {
            'status':'success',
            'emotion':emotion,
            'confidence':0.95
        }
    except Exception as e: #gom cac loi lai
        print(f"Lỗi: {e}")
        return {"status": "error", "emotion": "No Face", "confidence": 0}

@app.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket):
    pass

