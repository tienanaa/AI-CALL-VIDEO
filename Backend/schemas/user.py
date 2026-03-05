from pydantic import BaseModel

class UserCreaterRequest(BaseModel):
    username: str
    password: str

class UserLoginRequest(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    user_id:str
    username: str
    password: str
