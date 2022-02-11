from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

from app.database import Base

# Definig a schema for the request body
class PostBase(BaseModel):
    title: str
    content: str
    # Default value is set as True
    published: bool = True
    # Set the rating as an optional parameter with default value None
    #rating: Optional[int] = None

class GetPost(PostBase):
    created_at: datetime
    owner_id: int
    class Config:
        orm_mode = True

class CreatePost(PostBase):
    pass

class UpdatePost(PostBase):
    published: bool

class createUser(BaseModel):
    email: EmailStr
    password: str

class UserBase(BaseModel):
    email: EmailStr
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None