from datetime import datetime
from pydantic import BaseModel

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
    class Config:
        orm_mode = True

class CreatePost(PostBase):
    pass

class UpdatePost(PostBase):
    published: bool