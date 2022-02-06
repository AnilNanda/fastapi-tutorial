from .. import schemas, models, utils
from fastapi import Depends, HTTPException, status, FastAPI, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/users", tags=['Users'])

@router.post("/", response_model=schemas.UserBase)
def createuser(user: schemas.createUser, db: Session = Depends(get_db)):

    #hashing the user password before storing in DB
    user.password = utils.hash(user.password)

    new_user_query = models.User(**user.dict())
    db.add(new_user_query)
    db.commit()
    db.refresh(new_user_query)
    return new_user_query

@router.get("/{id}", response_model=schemas.UserBase)
def getUser(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f"User with is {id} doesn't exist")
    return user