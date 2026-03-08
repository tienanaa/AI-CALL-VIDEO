from fastapi import APIRouter, WebSocket, WebSocketDisconnect #bắt sự kiện user ngắt kết nối
import uuid

# Nhập bộ quản lý phòng của bạn vào
from services.room_service import room_manager

#dùng để quản lý và nhóm các đường dẫn API (routes)
router = APIRouter()

@router.post("/create-room")
async def create_room_endpoint(request_data: dict):
    room_name=request_data.get("room_name","Phòng mặc định")
    host_id=request_data.get("host_id")

    # Tạo ID phòng ngẫu nhiên 6 ký tự
    generated_room_id = str(uuid.uuid4())[:6]

    success = room_manager.create_room(
        room_id=generated_room_id, 
        room_name=room_name, 
        host_id=host_id
    )

    if success:
        return {"success": True, "room_id": generated_room_id, "message": "Tạo phòng thành công!"}
    return {"success": False, "message": "Lỗi khi tạo phòng"}

@router.websocket("/ws/{room_id}/{client_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str, client_id: str):
    
    is_connected = await room_manager.connect(websocket, room_id, client_id)
    if not is_connected:
        return 
    
    try:
        while True:
            # Nhận JSON và ném sang cho người kia
            data = await websocket.receive_json()
            await room_manager.broadcast(data, room_id, websocket)
            
    except WebSocketDisconnect:
        await room_manager.disconnect(websocket, room_id, client_id)
