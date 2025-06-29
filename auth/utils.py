from datetime import timedelta, datetime,timezone,date
from jose import JWTError, jwt
from passlib.context import CryptContext
from typing import Optional
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer,HTTPBearer,HTTPAuthorizationCredentials
from fastapi import FastAPI, Depends, HTTPException, status
from Models.tables import User,Task,WorkLog
from sqlalchemy import func
from sqlalchemy.orm import Session
from Models.database import get_db,SessionLocal
from User.user_schemas import UserBase

oauth2_scheme=HTTPBearer()
pwd_context=CryptContext(schemes=["bcrypt"])

class Token(BaseModel):
    access_token:str
    token_type:str

class Users(User):
    hashed_pass:str

secret_key="This is the secret key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=20


## Creates a hashed version of the password
def hash_password(password:str):
    if not password:
        raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Please enter a valid password"
            )
    return pwd_context.hash(password)


## Verifies the password with it's hashed version for authentication 
def verify_passsword(password,hashed_password):
    return pwd_context.verify(password,hashed_password)


## Gets the user from the database based on the user_id entered
def get_user(user_id:str, db:Session=Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        return {"Error":"Record not found"}
    return user


## Authenticates the presence of user in the database for verification 
def authenticate_user(userid:str,password:str,db):
    user = db.query(User).filter(User.user_id == userid).first()
    if not user or not verify_passsword(password,user.password):
        return None
    return user 


## Creates access token to be used for the login 
def create_access_token(payload:dict,expire_time:Optional[timedelta]=timedelta(minutes=20)):
    to_encode=payload.copy()
    expire = datetime.now(timezone.utc) + expire_time
    to_encode.update({"exp":expire})
    access_token=jwt.encode(to_encode,secret_key,algorithm=ALGORITHM)
    return access_token


## Gets the current user from the payload of the token generated
def get_current_user(token:HTTPAuthorizationCredentials = Depends(oauth2_scheme),db:Session=Depends(get_db)):
    try:
        payload = jwt.decode(token.credentials, secret_key, algorithms=[ALGORITHM]) ## USER ID OF THE USER
        
        return payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

## Gets the employee ID of the ucrrent user from the payload of the token generated
def get_emp_id(id:str=Depends(get_current_user)):
    return id



## Function to generate a new user_id based on the pattern

def auto_generate_emp_id():
    with SessionLocal() as db:
        latest_employee = db.query(func.max(User.user_id)).first()[0]

        if latest_employee:
            latest_number = int(latest_employee.split('_')[1])
            new_number = latest_number + 1
        else:
            new_number = 1

        new_employee_id = f"EMP_{new_number:03}"
    return new_employee_id

auto_generate_emp_id()


## Function to generate a new task_id based on the pattern

def auto_generate_task_id():
    with SessionLocal() as db:
        latest_task = db.query(func.max(Task.task_id)).first()[0]

        if latest_task:
            latest_number = int(latest_task.split('_')[1])
            new_number = latest_number + 1
        else:
            new_number = 1

        new_task_id = f"TASK_{new_number:03}"

    return new_task_id

auto_generate_task_id()


## Function to generate a new worklog_id based on the pattern
def auto_generate_work_id():
    with SessionLocal() as db:
        latest_worklog = db.query(func.max(WorkLog.work_id)).first()[0]

        if latest_worklog:
            latest_number = int(latest_worklog.split('_')[1])
            new_number = latest_number + 1
        else:
            new_number = 1

        new_work_id = f"WORK_{new_number:03}"
    
    return new_work_id

auto_generate_work_id()


## Function to compare two dates 

from datetime import datetime

def compare_date_dates(date1, date2):
    # date1 = date1.date()
    # date2 = date2.date()

    if date1 > date2:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="From date cannot be before the To date"

        )
    else:
        pass

def compare_str_dates(date1,date2):
    date1 = date1.date()
    # date2 = date2.date()

    if date1 > date2:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Due date cannot be before the date at which the task is created"

        )
    else:
        pass

