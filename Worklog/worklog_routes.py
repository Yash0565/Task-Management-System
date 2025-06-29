from fastapi import FastAPI,APIRouter,Depends, HTTPException,status
from Worklog.worklog_crud import create_worklog,view_worklog
from requests import Session
from Worklog.worklog_schemas import WorklogBase
from Models.tables import WorkLog,Base
from datetime import datetime
from Models.database import SessionLocal
from Models.database import engine
from User.user_crud import is_admin
from auth.utils import get_emp_id
from Models.database import SessionLocal as db
from Task.task_routes import get_db

router=APIRouter(
    prefix="/worklog",
    tags=["Worklog"]
)

Base.metadata.create_all(bind=engine)


## EVERYONE
## To create a new worklog in the database for a task assigned by/to the currently logged in user
@router.post("/create")
def create_new_worklog(worklog:WorklogBase,empid:str=Depends(get_emp_id)):
    if not worklog.task_id or not worklog.task_id.strip():
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Task ID cannot be left blank"
            )
    if not worklog.work_date or not worklog.work_date.strip():
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Work Date cannot be left blank"
            )
    
    if not worklog.time_spent or not worklog.time_spent.strip():
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Time spent cannot be left blank"
            )
    db_worklog=create_worklog(worklog,empid)
    return {
        "message": "Worklog created successfully"
    }

## EVERYONE
## To view the details fo the worklog created for a task assigned by/to the currently logged in user
@router.get("/view")
def view_all_worklogs(empid:str=Depends(get_emp_id)):
    result=view_worklog(empid)
    return result
