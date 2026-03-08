from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.rooms={} 
    
    #Tao phong moi
    def create_room(self,room_id: str,room_name:str,host_id: str  ):
        if room_id not in self.rooms:
            self.rooms[room_id]={
                "room_name": room_name,
                "host_id": host_id,
                "host_ws": None,
                "guest_ws":None
            }
            return True
        return False

    # Xu ly nguoi dung khi tham gia phong
    async def connect(self, websocket: WebSocket, room_id: str, client_id:str):
        # Kiểm tra phòng có tồn tại không
        if room_id not in self.rooms:
            await websocket.close(code=4004, reason="Phòng không tồn tại")
            return False
        
        room = self.rooms[room_id]
 
        # Nếu ID của người đang kết nối khớp với ID người tạo phòng
        if client_id == room["host_id"]:
            await websocket.accept()
            room["host_ws"] = websocket
            return True

        #  Kiểm tra xem ghế khách đã có ai ngồi chưa
        if room["guest_ws"] is not None:
            await websocket.close(code=4003, reason="Phòng đã đầy")
            return False

        # Xếp ghế cho KHÁCH
        await websocket.accept()
        room["guest_ws"] = websocket
        return True
    
    # Nếu cái phòng mà mình muốn tắt/ thoát nó mà vẫn còn ở trong danh sách phòng 
    # => ktra xem còn ko, còn bao nhiêu người => xóa nó
    async def disconnect(self, websocket: WebSocket, room_id: str,client_id:str):
        if room_id in self.rooms:
            room = self.rooms[room_id]

            if websocket == room["host_ws"]:
                print("Trưởng phòng thoát. Đóng cửa phòng!")
                # Neu con khach o trong, thi duoi khach ra

                if room["guest_ws"]:
                    try:
                        await room["guest_ws"].close(code=4000, reason="Host out")
                    except:
                        pass
                del self.rooms[room_id]

            # Neu nguoi thoat la khach
            elif websocket == room["guest_ws"]:
                print("Khách thoát. Giữ nguyên phòng để đón khách khác.")
                room["guest_ws"] = None

    #Vua la gui tin nhan, va gui thong so tin hieu
    async def broadcast(self, data: dict, room_id:str, sender_ws: WebSocket):
        if room_id in self.rooms:
            room = self.rooms[room_id]

            if sender_ws==room["host_ws"]:
                if room["guest_ws"] is not None:
                    await room["guest_ws"].send_json(data)
            #Van nen kiem tra de de phong xam nhap va bug
            elif sender_ws==room["guest_ws"]:
                if room["host_ws"] is not None:
                    await room["host_ws"].send_json(data)

# Khởi tạo một đối tượng duy nhất để [Dùng Chung] cho toàn hệ thống
#=> người quản lí chung
room_manager = ConnectionManager()