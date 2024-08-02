from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional
class PostBase(BaseModel):
    title:str
    content:str
    published:bool=True
    owner_id:int

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id:int
    created_at:datetime
    owner_id:int
    class config:
        orm_mode=True

class UserCreate(BaseModel):
    email:EmailStr
    password:str

class CreateUserResponse(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime
    class config:
        orm_mode=True

class GetUserResponse(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime
    class config:
        orm_mode=True


class user_login(BaseModel):
    email:EmailStr
    password: str

class token(BaseModel):
    access_token:str
    token_type: str

class token_data(BaseModel):
    id:Optional[int]