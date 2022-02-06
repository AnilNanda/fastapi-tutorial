from os import access
from fastapi import APIRouter, Depends, HTTPException, status
from .. import database, schemas, models, utils, oauth2
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=['Authentication'])

@router.post("/login")
def userLogin(usercredentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == usercredentials.username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {usercredentials.username} not authorised")
    if not utils.verify(usercredentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {usercredentials.username} not authorised")
    
    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}