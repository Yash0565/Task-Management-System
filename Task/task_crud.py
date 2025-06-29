from Task.task_schemas import TaskBase,UpdateTask
from fastapi import Depends,HTTPException,status
from typing import Optional
from Models.database import SessionLocal
from Models.tables import Task,taskStatusEnum,User
from datetime import datetime, date
from Models.database import get_db
from sqlalchemy.orm import Session
from auth.utils import get_emp_id,auto_generate_task_id,compare_str_dates

## Function to create a new task in the database 
def create_task(task:TaskBase, task_creator: str):
    db = SessionLocal()
    try:
        parsed_due_date = datetime.strptime(task.due_date, "%d-%m-%Y").date()
        tasks=db.query(Task).filter(User.user_id == task.assigned_to).first()
        if not tasks:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This Employee ID does not exist"
            )
        
        new_id=auto_generate_task_id()
        db_task=Task(
                task_id=new_id,

                task_name=task.taskname,
                desc=task.desc,
                assignedBy=task_creator,
                assignedTo=task.assigned_to,
                due_date=parsed_due_date,
                status=task.status,
                task_created_at=datetime.now(),
                task_updated_at=datetime.now()
            )
        if db_task.assignedTo==task_creator:

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot assign task to yourself"
            )
        compare_str_dates(tasks.task_created_at,parsed_due_date)
        db.add(db_task)
        db.commit()
        return db_task
    
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Please enter date in a valid format i.e (DD-MM-YYYY)"
        )
    
    finally:
        db.close()


## Function to view the tasks assigned to/by the current user 
def view_task(empid:str):
    try:
        with SessionLocal() as db:
            tasks=db.query(Task).join(User, Task.assignedBy == User.user_id).filter((Task.assignedBy == empid) | (Task.assignedTo == empid)).order_by(User.name).all()

            if not tasks:
                raise HTTPException(
                    status_code=404,
                    detail="No tasks found for the given employee ID"
                )
            

            formatted_tasks = []
            for task in tasks:
                assigner=db.query(User).filter(User.user_id==task.assignedBy).first()
                assignee=db.query(User).filter(User.user_id==task.assignedTo).first()
                formatted_tasks.append({
                    "Assigned By": assigner.name,
                    "Assigned To": assignee.name,
                    "Task ID": task.task_id,
                    "Name":task.task_name,
                    "Description": task.desc,
                    "Due date":task.due_date.strftime("%d-%m-%Y"),                
                    "Status":task.status,
                    "Created At": task.task_created_at.strftime("%d-%m-%Y %H:%M:%S")
                })
            return formatted_tasks   
    # except Exception as e:
    #     raise HTTPException(
    #         status_code=500,
    #         detail=f"An error occurred while fetching users: {str(e)}"
    #     )
    finally:
        db.close()
    

## Function to delete a task record form the database
def delete_task(taskid:str):
    with SessionLocal() as db: 
        task=db.query(Task).filter(Task.task_id==taskid).first()
        if not task:
            raise HTTPException(
                    status_code=404,
                    detail="Task not found"
            )
        db.delete(task)
        db.commit()
        return {"Message": "Task deleted successfully"}
    


## Function to update the task record in the database
def update_task(
        taskid:str,
        taskname:Optional[str],
        taskdesc:Optional[str],
        assigned_to:Optional[str],
        due_date:Optional[str],
        taskstatus:Optional[taskStatusEnum],
        empid:str
        ):
    try:
        with SessionLocal() as db:
            task=db.query(Task).filter((Task.assignedBy==empid) & (Task.task_id==taskid)).first()
            if not task:
                raise HTTPException(
                        status_code=404,
                        detail="Can only modify tasks which are assigned by you"
                    )
                
            if taskname is not None:
                task.task_name=taskname
            if taskdesc is not None:
                task.desc=taskdesc
            if assigned_to is not None:
                present=db.query(User).filter(User.user_id == assigned_to).first()
                if assigned_to==empid:
                    raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Cannot assign task to yourself"
                )

                if not present:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Employee does not exist"
                    )

                task.assignedTo=assigned_to
            if due_date is not None:
                parsed_due_date = datetime.strptime(due_date, "%d-%m-%Y").date()
                compare_str_dates(task.task_created_at,parsed_due_date)
                task.due_date=parsed_due_date
            if taskstatus is not None:
                task.status=taskstatus
            task.task_updated_at=datetime.now()
            db.commit()
            return(task)
            
        return(task)
    except ValueError:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Due date should be of the format (DD-MM-YYYY)"
            )
    
## Function to update the task status in the database
def update_status(taskid:str,status:taskStatusEnum,empid:str):
    with SessionLocal() as db:
            task=db.query(Task).filter((Task.task_id==taskid) & ((Task.assignedBy == empid) | (Task.assignedTo == empid))).first()
            if not task:
                raise HTTPException(
                    status_code=404,
                    detail="Can only modify tasks which are assigned to/by you"
                )
            if task:
                task.status = status
                task.task_updated_at=datetime.now()
                db.commit()
                db.refresh(task)
            return {"Message": "Record updated successfully"}
            


