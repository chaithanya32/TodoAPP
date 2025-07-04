from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel, Field
from starlette import status  
from sqlalchemy.orm import Session
from typing_extensions import Annotated
from ..database import SessionLocal
from ..models import Todos
from .auth import get_current_user

# Initialize router
router = APIRouter(
    prefix='/admin',
    tags=['admin']
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

@router.get("/todo",status_code=status.HTTP_200_OK)
async def read_all(user:user_dependency, db:db_dependency ):
    if user is None or user.get('user_role')!='admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    return db.query(Todos).all()

@router.delete("/todo/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user:user_dependency, db:db_dependency, todo_id:int= Path(gt=0)):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=401, detail="Authentication Failed")
    
    todo_model=db.query(Todos).filter(Todos.id==todo_id).first()

    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not Found')
    
    db.query(Todos).filter(Todos.id==todo_id).delete()
    db.commit()