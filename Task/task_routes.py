from fastapi import FastAPI,APIRouter,Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from requests import Session
from typing import Optional
from Task.task_schemas import TaskBase,UpdateTask
from Models.tables import User,Base,Task,taskStatusEnum
from datetime import timedelta, datetime
from Models.database import SessionLocal
from User.user_crud import is_admin
from Models.database import engine
from Task.task_crud import create_task,view_task,delete_task,update_task,update_status
from datetime import date
from auth.utils import get_current_user,create_access_token,authenticate_user,get_user,verify_passsword,hash_password,get_emp_id,ACCESS_TOKEN_EXPIRE_MINUTES, oauth2_scheme
from Models.database import SessionLocal as db

router=APIRouter(
    prefix="/task",
    tags=["Task Management"]
)

def get_db():
    db = SessionLocal()  # Create a new session instance
    try:
        yield db
    finally:
        db.close()

Base.metadata.create_all(bind=engine)

## EVERYONE
## To create a new task
@router.post("/create")
def register_task(task:TaskBase,empid: str = Depends(get_emp_id)):
    if not task.taskname or not task.taskname.strip():
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Task name cannot be left blank"
            )
    if not task.assigned_to or not task.assigned_to.strip():
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="'Assigned To' field cannot be left blank"
            )
    if not task.due_date or not task.due_date.strip():
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Due date cannot be left blank"
            )
    create_task(task,empid)
    return {"Message":"Task created successfully"}


## EVERYONE
## To display the tasks where the current user has either assigned a task or received one
@router.get("/view")
def view_task_details(empid:str = Depends(get_emp_id)):
    result=view_task(empid)
    return result


## ADMINS ONLY
## To delete a task record from the database
@router.delete("/delete")
def delete_task_record(taskid:str,authorized: bool = Depends(is_admin)):
    if not authorized:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to perform this action"
        )
    delete_task(taskid)
    return{"Message":"Record deleted successfully"}
    


## ONLY BY USER WHO ASSGINED THE TASK
## To update the details of a single task record in the database
@router.put("/update")
def update_task_details(
    taskid:str,
    taskname:Optional[str]= None,
    taskdesc:Optional[str]= None,
    assigned_to:Optional[str]= None,
    due_date:Optional[str]= None,
    taskstatus:Optional[taskStatusEnum]= None,
    empid: str = Depends(get_emp_id)
    ):
    result=update_task(taskid,taskname,taskdesc,assigned_to,due_date,taskstatus,empid)
    return {"Message":"Task Details updated successfully"}
    


## ONLY BY THE USER WHO ASSIGNED THE TASK AND THE USER WHO RECEIVED IT
## To update the status of the task in the database
@router.put("/update/status")
def update_task_status(taskid:str,status:taskStatusEnum,empid:str=Depends(get_emp_id)):
    return update_status(taskid,status,empid)