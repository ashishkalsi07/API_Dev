from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
import models, schemas
from database import get_db
import utility

router=APIRouter(
    prefix="/users",
    tags=['users']
)

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.CreateUserResponse)
def create_user(user:schemas.UserCreate,db: Session = Depends(get_db)):
    # hash the password first - user.password
    hashed_password =  utility.hash(user.password)
    user.password = hashed_password   
    new_user = models.user(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}",response_model=schemas.GetUserResponse)
def user(id:int,db: Session = Depends(get_db)):
    user = db.query(models.user).filter(models.user.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id: {id} does not exist")
    
    return user