from random import randrange
from typing import Optional
from urllib import response
from fastapi import FastAPI, Response, status, HTTPException
#from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time

my_post = [{"id":1,"title":"First Post Title","content":"First Post content"}]

app = FastAPI()

# Definig a schema for the request body
class Post(BaseModel):
    title: str
    content: str
    # Default value is set as True
    published: bool = True
    # Set the rating as an optional parameter with default value None
    rating: Optional[int] = None

while True:
    try:
        conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='postgres',cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("DB connection success")
        break
    except Exception as error:
        print("DB connection failed",error)
        time.sleep(10)



def find_post(id):
    for post in my_post:
        if post["id"] == id:
            return post

def find_index(id):
    for post in my_post:
        if post["id"] == id:
            return my_post.index(post)

@app.get("/")
def getPost():
    return {"message":"Hello World!"}


@app.get("/posts")
def getPost():
    cursor.execute("""SELECT * FROM posts """)
    dbposts = cursor.fetchall()
    return {"data" : dbposts}

# Default response status is set as parameter to the decorator
@app.post("/posts", status_code=status.HTTP_201_CREATED)

# The body of the request is stored in variable payload and validated again the schema Post defined above
def createPost(payload: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) values(%s, %s, %s) RETURNING *""",(payload.title, payload.content, payload.published, ))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}

@app.get("/posts/{id}")

# id: int ensures the id value passed in the request is int type
def getpost(id: int):
    cursor.execute("""SELECT * FROM posts where id = %s""",(id,))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message": f"post with id: {id} not found"}
    return {"data": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletepost(id: int):
    cursor.execute("""SELECT * FROM posts where id = %s""", (id,))
    index = cursor.fetchone()
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")
    #my_post.pop(index)
    cursor.execute("""DELETE FROM posts where id = %s RETURNING *""", (id,))
    conn.commit()
    # delete request can't return any response back to user, it can return only a status
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def updatepost(id: int, payload: Post):
    cursor.execute("""SELECT * FROM posts where id = %s""", (id,))
    index = cursor.fetchone()
    if index == None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post not found with id {id}")
    cursor.execute("""UPDATE posts SET title=%s, content=%s, published=%s WHERE id = %s RETURNING *""", (payload.title,payload.content,payload.published, id))
    conn.commit()
    return {"message": "updated post"}