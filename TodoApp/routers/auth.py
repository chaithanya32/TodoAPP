from datetime import datetime, timedelta, timezone
from typing_extensions import Annotated
from fastapi import APIRouter, Depends, HTTPException ,status ,Request
from pydantic import BaseModel
from ..database import SessionLocal
from ..models import Users
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm ,OAuth2PasswordBearer
from jose import jwt ,JWTError
from fastapi.templating import Jinja2Templates

router=APIRouter(
    prefix='/auth',
    tags=['auth']
)

SECRET_KEY='384d664272633ba48f427a5b441f313a29009c41a7203c5148e8f61f7ee1c874'
ALGORITHM='HS256'

bcrypt_context=CryptContext(schemes=['bcrypt'],deprecated='auto')
oauth2_bearer=OAuth2PasswordBearer(tokenUrl='auth/token')


class createUserRequest(BaseModel):
    username:str
    email:str
    first_name:str
    last_name:str
    password:str
    role:str
    phone_number:str

class Token(BaseModel):
    access_token:str
    token_type:str

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Annotated type for dependency injection
db_dependency = Annotated[Session, Depends(get_db)]

templates=Jinja2Templates(directory="TodoApp/templates")

### pages ###
@router.get("/login-page")
def render_login_page(request:Request):
    return templates.TemplateResponse("login.html", {'request':request})

@router.get("/register-page")
def render_login_page(request:Request):
    return templates.TemplateResponse("register.html", {'request':request})



### EndPoints ###
def authenticate_user(username:str,password:str,db):
    user=db.query(Users).filter(Users.username==username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password,user.hashed_password):
        return False
    return user 


def create_access_token(username: str, user_id: int,role:str, expires_delta: timedelta):
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {'sub': username, 'id': user_id, 'exp': expire, 'role':role}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)



async def get_current_user(token: Annotated[str,Depends(oauth2_bearer)]):
    try:
        payload=jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username:str= payload.get('sub')
        user_id:int = payload.get('id')
        user_role = payload.get('role')

        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user.')
        return {'username':username, 'id':user_id, 'user_role':user_role}
    
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user.')



@router.post("/",status_code=status.HTTP_201_CREATED)
async def create_user(db:db_dependency,create_user_request:createUserRequest):
    create_user_model=Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        is_active=True,
        phone_number=create_user_request.phone_number
    )


    db.add(create_user_model)
    db.commit()


@router.post("/token",response_model=Token)
async def login_for_access_token(form_data:Annotated[OAuth2PasswordRequestForm,Depends()],db :db_dependency):
    user=authenticate_user(form_data.username,form_data.password,db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user.')
    token=create_access_token(user.username, user.id, user.role, timedelta(minutes=20))

    return {'access_token':token, 'token_type':'bearer'}
