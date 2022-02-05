from random import randrange
from typing import Optional
from fastapi import FastAPI
#from fastapi.params import Body
from pydantic import BaseModel


my_post = [{"id":1,"title":"First Post","content":"First Post content"}]

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

def find_post(id):
    for post in my_post:
        if post["id"] == id:
            return post

@app.get("/")
def getPost():
    return {"message":"Hello World!"}


@app.get("/posts")
def getPost():
    return {"data" : my_post}

@app.post("/posts")
def createPost(payload: Post):
    #print(payload,payload.dict())
    post = payload.dict()
    post["id"] = randrange(0,10000)
    my_post.append(post)
    return {"data": post}

@app.get("/posts/{id}")
def getpost(id: int):
    post = find_post(id)
    return {"data": post}


    