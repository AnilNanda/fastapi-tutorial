from fastapi import APIRouter, Depends, HTTPException, status
from .. import database, schemas, models, utils
from sqlalchemy.orm import Session

router = APIRouter(tags=['Authentication'])

@router.post("/login")
def userLogin(usercredentials: schemas.UserLogin, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == usercredentials.email).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {usercredentials.email} not authorised")
    if not utils.verify(usercredentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {usercredentials.email} not authorised")