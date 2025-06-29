from User.user_schemas import UserBase
from fastapi import Depends,HTTPException,status
from Models.database import SessionLocal
from Models.tables import User, Task, WorkLog
from datetime import datetime
from Models.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from auth.utils import get_emp_id,auto_generate_emp_id
from typing import Optional


class DuplicateError(Exception):
    pass



## Function to create a new user in the database
def create_user(user:UserBase):

    with SessionLocal() as db:
        if not (len(user.mobile) == 10 and user.mobile.isdigit()):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Please enter a valid 10-digit mobile number"
            )
        
        try:
            mobile_record=db.query(User).filter((User.mobile==user.mobile)).first()
            if mobile_record:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Mobile Number already exists"
                ) 
            
            email_record=db.query(User).filter((User.email==user.email)).first()
            if email_record:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already exists"
                ) 
            
            new_id=auto_generate_emp_id()
            db_user = User(
                user_id=new_id,
                name=user.username,
                password=user.password,
                mobile=user.mobile,
                email=user.email.lower(),
                role=user.role,    
                status=user.status,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            db.add(db_user)
            db.commit()
            db.refresh(db_user)  
            return {"Message":"User saved successfully"}
         
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with the same user ID already exists."
            )
            
        finally:
            db.close()  

## Function to view the details of a specific user
def view_user(userid:str):
    with SessionLocal() as db:
        user=db.query(User).filter(User.user_id==userid).first()
        try:
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="This record does not exist in the database"
                )
            return {"Employee ID": user.user_id,"Name":user.name, "Email": user.email,"Mobile":user.mobile}
        
        finally:
            db.close()

## Function to view the details of all the users 
def view_all_users(userid:Optional[str]=None):
    with SessionLocal() as db:
        
        if userid:
            user=db.query(User).filter(User.user_id==userid).first()
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="This record does not exist in the database"
                )
            return {"Name":user.name,"Employee ID": user.user_id, "Email": user.email,"Mobile":user.mobile}
        else:
            users=db.query(User).order_by(User.name).all()
            employees=[]
            for emp in users:
                employees.append({"Name":emp.name,"Employee ID": emp.user_id, "Email": emp.email,"Mobile":emp.mobile})
            return employees

            


## Function to delete the record of a specific user 
def delete_user(userid:str):

    with SessionLocal() as db:
        user = db.query(User).filter(User.user_id == userid).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="This Employee does not exist"
            )
        tasks=db.query(Task).filter((user.user_id==Task.assignedBy) | (user.user_id==Task.assignedTo)).all()

        worklogs=db.query(WorkLog).filter((user.user_id==WorkLog.user_id)).all()

        for worklog in worklogs:
            db.delete(worklog)
        for task in tasks:
            db.delete(task)

        
        db.delete(user)
        db.commit()
               

## Function to update the details of a specific user
def update_user(userid:str,new_mobile:str):
    with SessionLocal() as db:
        user = db.query(User).filter(User.user_id == userid).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee does not exist"
            )
        if not (len(new_mobile) == 10 and new_mobile.isdigit()):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Please enter a valid 10-digit mobile number"
            )
        mobile_record=db.query(User).filter((User.mobile==user.mobile)).first()
        if mobile_record:
            raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Mobile Number already exists"
                ) 
            
        email_record=db.query(User).filter((User.email==user.email)).first()
        if email_record:
            raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already exists"
                ) 

        user.mobile=new_mobile
        db.commit()

## Function to check if the current logged in user is an admin
def is_admin(userid:str=Depends(get_emp_id),db:Session=Depends(get_db)):
    user = db.query(User).filter(User.user_id.ilike(userid)).first()
    if user and user.role.value.lower() == "admin":
        return True
    return False
