from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel, Field
from starlette import status  
from sqlalchemy.orm import Session
from typing_extensions import Annotated
from ..database import SessionLocal
from ..models import Todos, Users
from .auth import get_current_user
from passlib.context import CryptContext

# Initialize router
router = APIRouter(
    prefix='/user',
    tags=['user']
)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Annotated type for dependency injection
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency=Annotated[dict,Depends(get_current_user)]

bcrypt_context=CryptContext(schemes=['bcrypt'],deprecated='auto')


class userVerification(BaseModel):
    password:str
    new_password:str =Field(min_length=6)



@router.get("/",status_code=status.HTTP_200_OK)
async def get_user(user:user_dependency, db:db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(Users).filter(Users.id==user.get('id')).first()


@router.put("/password",status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user:user_dependency, db:db_dependency, user_verification: userVerification):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    user_model=db.query(Users).filter(Users.id==user.get('id')).first()

    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail='Error on changing password')
    
    user_model.hashed_password=bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()


@router.put("/phonenumber/{phone_number}",status_code=status.HTTP_204_NO_CONTENT)
async def change_phone_number(user:user_dependency, db:db_dependency, phone_number:str):
     if user is None:
         raise HTTPException(status_code=401, detail='Authentication Failed')
     
     user_model=db.query(Users).filter(Users.id==user.get('id')).first()
     user_model.phone_number=phone_number
     db.add(user_model)
     db.commit()    