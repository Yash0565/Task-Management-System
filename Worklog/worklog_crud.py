from Worklog.worklog_schemas import WorklogBase
from fastapi import Depends,HTTPException,status
from typing import Optional
from Models.database import SessionLocal
from Models.tables import WorkLog, Task
from datetime import datetime, date, time,timedelta
from Models.database import get_db
from sqlalchemy.orm import Session
from auth.utils import get_emp_id,auto_generate_work_id
from sqlalchemy.exc import IntegrityError

## Function to create a new worklog in the system
def create_worklog(worklog:WorklogBase,empid:str):
    try:
        db=SessionLocal()

        record=db.query(Task).filter((Task.assignedBy == empid) | (Task.assignedTo == empid)).all()

        task_ids = [task.task_id for task in record]

        if worklog.task_id not in task_ids:
            raise HTTPException(
                    status_code=403,
                    detail="You are not authorized to create worklog for this task"
                )
        
        try:
            parsed_due_date = datetime.strptime(worklog.work_date, "%d-%m-%Y").date()
        except ValueError:
            raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Please enter date in a valid format i.e (DD-MM-YYYY)"
        )
        try:
            parsed_duration = datetime.strptime(worklog.time_spent, "%H:%M")
        except ValueError:
            raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Please enter time in a valid format i.e (HH:MM)"
        )
        time_obj = time(parsed_duration.hour, parsed_duration.minute, 0)
        new_work_id=auto_generate_work_id()
        db_worklog=WorkLog(
                work_id=new_work_id,
                user_id=empid,
                task_id=worklog.task_id,
                work_date=parsed_due_date,
                time_spent=time_obj,
                created_at=datetime.now()
            )
            
        test=calc_work_hours(new_work_id,worklog.task_id,parsed_due_date,time_obj,empid)


        db.add(db_worklog)
        db.commit()
        return {"worklog_id": db_worklog.work_id}
    
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Please enter date in a valid format i.e (DD-MM-YYYY)"
        )
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Given Work ID already exists"
        )
    
    
## Function to view the worklogs by the user who has created or received a task
def view_worklog(empid:str):
    db=SessionLocal()
    try:
        records=db.query(Task).filter((Task.assignedBy == empid) | (Task.assignedTo == empid)).all()

        task_ids = [task.task_id for task in records]

        worklogs=db.query(WorkLog).filter(WorkLog.task_id.in_(task_ids) ).all()

        authorized_logs = [log for log in worklogs if log.task_id in task_ids]

        if not authorized_logs:
            raise HTTPException(
                status_code=403,
                detail="You are not authorized to view this worklog"
            )
        formatted_logs=[]
        for logg in authorized_logs:
            
            formatted_logs.append({
                "Work ID":logg.work_id,
                "Task ID":logg.task_id,
                "User":logg.user.name,
                "Work Date":logg.work_date.strftime("%d-%m-%Y"),
                "Time Spent":logg.time_spent,
                "Created at":logg.created_at.strftime("%d-%m-%Y %H:%M:%S")

            })
        return formatted_logs 
    
    finally:
        db.close()

def calc_work_hours(workid:str,task_id:str, work_date: datetime.date, time_obj: datetime.time,empid:str):
    db=SessionLocal()
    try:
        logs = db.query(WorkLog).filter(
            WorkLog.user_id == empid,
            WorkLog.task_id == task_id,
            WorkLog.work_date == work_date
        ).all()

        total_duration = sum((time_to_timedelta(log.time_spent) for log in logs), timedelta())
        spent=time_to_timedelta(time_obj)
        if total_duration + spent > timedelta(hours=24):
            raise HTTPException(
                status_code=400,
                detail="Cannot log more than 24 hours on a single task on same day."
            )
        
    finally:
        db.close()
        

    
def time_to_timedelta(t: datetime.time):
    return timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)