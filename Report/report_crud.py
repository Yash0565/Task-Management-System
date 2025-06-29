from Task.task_schemas import TaskBase
from fastapi import Depends,HTTPException
from typing import Optional
from Models.database import SessionLocal
from datetime import datetime, date
from Models.tables import Task
from Models.database import get_db
from sqlalchemy.orm import Session
from auth.utils import get_emp_id,compare_date_dates


## Function to generate a report for ADMINS only with all the task records with various filters
def admin_report(
        assigner_id: Optional[str] = None,
        assignee_id: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None
        ):
    
    db=SessionLocal()
    try:
        query = db.query(Task)
        if assigner_id:
            query = query.filter(Task.assignedBy == assigner_id)
        if assignee_id:
            query = query.filter(Task.assignedTo == assignee_id)
        if from_date:
            parsed_from_date = datetime.strptime(from_date, "%d-%m-%Y").date()
            query = query.filter(Task.due_date >= parsed_from_date)
        if to_date:
            parsed_to_date = datetime.strptime(to_date, "%d-%m-%Y").date()
            query = query.filter(Task.due_date <= parsed_to_date)
        if from_date and to_date:
            compare_date_dates(parsed_from_date,parsed_to_date)
        result= query.all()
        if not result:
            raise HTTPException(
                status_code=404,
                detail="No records found with the given filters"
            )
        admin_record=[]
        for report in result:
            admin_record.append({
                "Task ID":report.task_id,
                "Assigned by":report.assignedBy,
                "Assigned to":report.assignedTo,
                "Due date":report.due_date.strftime("%d-%m-%Y"),
                "Description":report.desc,
                "Completion Status":report.status,
                "Task created at":report.task_created_at.strftime("%d-%m-%Y %H:%M:%S")
            })
        return admin_record
    
    except ValueError:
        raise HTTPException(
            status_code=422,
            detail="Invalid date format. Use DD-MM-YYYY for both from_date and to_date."
        )

    finally:
        db.close()



## Function to generate a report of all the tasks assigned by the current user
def assigner_report(
        assigner_id: str,
        assignee_id: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None
):
    db=SessionLocal()
    try:
        query = db.query(Task)
        query = query.filter(Task.assignedBy == assigner_id)
        if assignee_id:
            query = query.filter(Task.assignedTo == assignee_id)
        if from_date:
            parsed_from_date = datetime.strptime(from_date, "%d-%m-%Y").date()
            query = query.filter(Task.due_date >= parsed_from_date)
        if to_date:
            parsed_to_date = datetime.strptime(to_date, "%d-%m-%Y").date()
            query = query.filter(Task.due_date <= parsed_to_date)

        if from_date and to_date:
            compare_date_dates(parsed_from_date,parsed_to_date)
        result= query.all()
        if not result:
            raise HTTPException(
                status_code=404,
                detail="No records found with the given filters"
            )
        assigner_record=[]
        for report in result:
            assigner_record.append({
                "Task ID":report.task_id,
                "Assigned by":report.assignedBy,
                "Assigned to":report.assignedTo,
                "Due date":report.due_date.strftime("%d-%m-%Y"),
                "Description":report.desc,
                "Completion Status":report.status,
                "Task created at":report.task_created_at.strftime("%d-%m-%Y %H:%M:%S")
            })
        return assigner_record
    
    except ValueError:
        raise HTTPException(
            status_code=422,
            detail="Invalid from_date format. Use DD-MM-YYYY."
        )
    
    finally:
        db.close()


## Function to generate a report of all the tasks assigned to the current user
def assignee_report(
        assignee_id: str,
        assigner_id: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None
):
    db=SessionLocal()
    try:
        query = db.query(Task)
        query = query.filter(Task.assignedTo == assignee_id)

        if assigner_id:
            query = query.filter(Task.assignedBy == assigner_id)
        if from_date:
            parsed_from_date = datetime.strptime(from_date, "%d-%m-%Y").date()
            query = query.filter(Task.due_date >= parsed_from_date)
        if to_date:
            parsed_to_date = datetime.strptime(to_date, "%d-%m-%Y").date()
            query = query.filter(Task.due_date <= parsed_to_date)

        if from_date and to_date:
            compare_date_dates(parsed_from_date,parsed_to_date)
        result= query.all()
        if not result:
            raise HTTPException(
                status_code=404,
                detail="No records found with the given filters"
            )
        assignee_record=[]
        for report in result:
            assignee_record.append({
                "Task ID":report.task_id,
                "Assigned by":report.assignedBy,
                "Assigned to":report.assignedTo,
                "Due date":report.due_date.strftime("%d-%m-%Y"),
                "Description":report.desc,
                "Completion Status":report.status,
                "Task created at":report.task_created_at.strftime("%d-%m-%Y %H:%M:%S")
            })
        return assignee_record
    
    except ValueError:
        raise HTTPException(
            status_code=422,
            detail="Invalid from_date format. Use DD-MM-YYYY."
        )
    
    finally:
        db.close()