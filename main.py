from typing import Optional
from fastapi import FastAPI
#from fastapi.params import Body
from pydantic import BaseModel


my_post = [{"title":"First Post","content":"First Post content"}]

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


@app.get("/")
def getPost():
    return {"message":"Hello World!"}


@app.get("/posts")
def getPost():
    return {"data" : my_post}

@app.post("/posts")
def createPost(payload: Post):
    print(payload,payload.dict())
    return {"message": f"title: {payload.title}, content {payload.content}"}