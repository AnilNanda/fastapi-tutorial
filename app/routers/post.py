from .. import schemas, models, oauth2
from ..database import get_db, SessionLocal
from sqlalchemy.orm import Session
from fastapi import Depends, status, HTTPException, Response, APIRouter
from typing import List

router = APIRouter(prefix="/posts", tags=['Posts'])


@router.get("/",response_model=List[schemas.GetPost])
def getPost(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    dbposts = db.query(models.Post).all()
    return dbposts

# Default response status is set as parameter to the decorator
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.GetPost)

# The body of the request is stored in variable payload and validated again the schema Post defined above
def createPost(payload: schemas.CreatePost, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # **payload.dict unpacks the Body and matches it with the model defined
    # print(**payload.dict())
    print(current_user.id)
    new_post = models.Post(owner_id=current_user.id, **payload.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}", response_model=schemas.GetPost)

# id: int ensures the id value passed in the request is int type
def getpost(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message": f"post with id: {id} not found"}
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletepost(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if post_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    # delete request can't return any response back to user, it can return only a status
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def updatepost(id: int, payload: schemas.UpdatePost, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if post_query.first() == None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post not found with id {id}")
    
    post_query.update(payload.dict(),synchronize_session=False)
    db.commit()
    return post_query.first()