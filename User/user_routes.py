from fastapi import FastAPI,APIRouter,Depends, HTTPException,status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from requests import Session
from User.user_schemas import UserBase
from Models.tables import User,Base
from datetime import timedelta, datetime
from Models.database import SessionLocal

from Models.database import engine
from User.user_crud import create_user, view_user, view_all_users, delete_user, update_user, is_admin
from auth.utils import get_current_user,create_access_token,authenticate_user,get_user,verify_passsword,ACCESS_TOKEN_EXPIRE_MINUTES, oauth2_scheme
from Models.database import SessionLocal as db
from typing import Optional

router=APIRouter(
    prefix="/user",
    tags=["User Management"]
)

router2=APIRouter(
    prefix="/Login",
    tags=["Login"]
)

def get_db():
    db = SessionLocal()  # Create a new session instance
    try:
        yield db
    finally:
        db.close()

Base.metadata.create_all(bind=engine)

pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

def hash_password(password):
    if not password or not password.strip():
        raise ValueError("Password must not be empty or just whitespace.")
    return pwd_context.hash(password)



## ADMINS ONLY
## To register a new user in the system
@router.post("/register")
def register_user(user:UserBase,authorized: bool = Depends(is_admin)):
    if not authorized:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to perform this action"
        )
    
    if not user.username or not user.username.strip().isalnum():
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Please enter a valid username"
            )
    if not user.password or not user.password.strip():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Password cannot be empty or blank."
        )
    user.password = hash_password(user.password) 
    new_user=create_user(user)
    return new_user
    

## ADMINS ONLY
## To view the detials of all the users in the database
@router.get("/display")
def view_all(userid:Optional[str]=None,authorized: bool = Depends(is_admin)):
    if not authorized:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to perform this action"
        )
    value=view_all_users(userid)
    return{"List of all users":value}
    
        

## ADMINS ONLY
## To delete the record of a user from the Database
@router.delete("/delete")
def delete_user_record(userid:str,authorized: bool = Depends(is_admin)):
    if not authorized:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to perform this action"
        )
    
    delete_user(userid)
    return{"Message":"Record deleted successfully"}
    


## ADMINS ONLY
## To update the details of a user in the database
@router.put("/update/{userid}")
def update_user_record(userid:str,mobile:str,authorized: bool = Depends(is_admin)):
    if not authorized:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to perform this action"
        )
    update_user(userid,mobile)
    return{"Message":"Record updated successfully"}
    
    
## EVERYONE 
## To login and receive a token
@router2.post("/token")
def login_for_token(userid:str,password:str, db: Session = Depends(get_db)):
    user=authenticate_user(userid,password,db)

    try:
        if not user:
            raise HTTPException(
                    status_code=401,
                    detail="Incorrect username or password",
                    headers={"WWW-Authenticate": "Bearer"},
                )
        access_token=create_access_token(
                {"sub": user.user_id}, 
                timedelta(minutes=20),
            )
        return {"access_token": access_token}

    except AttributeError:
        raise HTTPException(
                status_code=401,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
   
    
