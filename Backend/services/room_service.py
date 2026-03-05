from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connection: dict[str, list[WebSocket]]={} 
        # các mã phòng đang mở và các đường ống chỉ tới user
    
    # nếu ko tim thấy phòng thì tạo phòng mới bằng id đó luôn
    async def connect(self, websocket: WebSocket, room_id: str):
        await websocket.accept() 
        if room_id not in self.active_connection:
            self.active_connection[room_id]=[] 

        if len(self.active_connection[room_id])>=2:
            await websocket.close(code=4000, reason="Phòng đã đầy")
            return False
        
        self.active_connection[room_id].append(websocket)
        return True
    
        
        