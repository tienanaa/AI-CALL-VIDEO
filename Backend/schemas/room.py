from pydantic import BaseModel

class RoomRequest(BaseModel):
    room_name:str


class RoomCreateResponse(BaseModel):
    success: bool
    room_id: str
    message: str
    host_id:str