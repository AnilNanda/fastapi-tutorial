from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, authentication

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# while True:
#     try:
#         conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='postgres',cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("DB connection success")
#         break
#     except Exception as error:
#         print("DB connection failed",error)
#         time.sleep(10)

app.include_router(post.router)

app.include_router(user.router)

app.include_router(authentication.router)

@app.get("/")
def getPost():
    return {"message":"Hello World!"}