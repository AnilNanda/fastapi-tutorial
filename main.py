from fastapi import FastAPI
from fastapi.params import Body

my_post = [{"title":"First Post","content":"First Post content"}]

app = FastAPI()

@app.get("/")
def getPost():
    return {"message":"Hello World!"}


@app.get("/posts")
def getPost():
    return {"data" : my_post}

@app.post("/posts")
def createPost(payload: dict = Body(...)):
    return {"message":payload}
