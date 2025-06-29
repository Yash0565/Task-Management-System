from fastapi import FastAPI,APIRouter,Depends, HTTPException
from typing import Optional
from datetime import date
from Report.report_crud import admin_report,assigner_report,assignee_report
from User.user_crud import is_admin
from auth.utils import get_emp_id

router=APIRouter(
    prefix="/report",
    tags=["Reports"]
)

from Task.task_routes import get_db

## ADMINS ONLY
## To get all the records according to the vaious filters
@router.get("/filter")
def filter_records(
    assigner_id: Optional[str] = None,
        assignee_id: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        authorized: bool = Depends(is_admin)
        ):
    if not authorized:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to perform this action"
        )
    result=admin_report(assigner_id,assignee_id,from_date,to_date)
    return result
    

## ALL USERS
## To get all the records of tasks assigned by the current user
@router.get("/filter/assigner")
def filter_records(
    assigner_id: str=Depends(get_emp_id),
        assignee_id: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        ):
    result=assigner_report(assigner_id,assignee_id,from_date,to_date)
    return result
    

## ALL USERS
## To get all the records of tasks assigned to the current user
@router.get("/filter/assignee")
def filter_records(
    assignee_id: str=Depends(get_emp_id),
        assigner_id: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        ):

    result=assignee_report(assignee_id,assigner_id,from_date,to_date)
    return result