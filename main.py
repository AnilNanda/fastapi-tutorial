from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def getPost():
    return "Hello World!"