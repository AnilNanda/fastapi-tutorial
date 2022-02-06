from random import randrange
from typing import Optional
from urllib import response
from fastapi import FastAPI, Response, status, HTTPException, Depends
#from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session


#my_post = [{"id":1,"title":"First Post Title","content":"First Post content"}]

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Definig a schema for the request body
class Post(BaseModel):
    title: str
    content: str
    # Default value is set as True
    published: bool = True
    # Set the rating as an optional parameter with default value None
    #rating: Optional[int] = None

# while True:
#     try:
#         conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='postgres',cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("DB connection success")
#         break
#     except Exception as error:
#         print("DB connection failed",error)
#         time.sleep(10)

@app.get("/")
def getPost():
    return {"message":"Hello World!"}


@app.get("/posts")
def getPost(db: Session = Depends(get_db)):
    dbposts = db.query(models.Post).all()
    return {"data" : dbposts}

# Default response status is set as parameter to the decorator
@app.post("/posts", status_code=status.HTTP_201_CREATED)

# The body of the request is stored in variable payload and validated again the schema Post defined above
def createPost(payload: Post, db: Session = Depends(get_db)):
    # **payload.dict unpacks the Body and matches it with the model defined
    # print(**payload.dict())
    new_post = models.Post(**payload.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}

@app.get("/posts/{id}")

# id: int ensures the id value passed in the request is int type
def getpost(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message": f"post with id: {id} not found"}
    return {"data": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletepost(id: int, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if post_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    # delete request can't return any response back to user, it can return only a status
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def updatepost(id: int, payload: Post, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if post_query.first() == None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post not found with id {id}")
    
    post_query.update(payload.dict(),synchronize_session=False)
    db.commit()
    return {"message": post_query.first()}