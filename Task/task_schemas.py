from pydantic import BaseModel
from typing import Optional
from Models.tables import taskStatusEnum
from datetime import date
class TaskBase(BaseModel):
    taskname:str
    desc:Optional[str]
    assigned_to:str
    due_date: str
    status:taskStatusEnum

class UpdateTask(BaseModel):
    taskname:Optional[str]
    desc:Optional[str]
    assigned_to:Optional[str]
    due_date:Optional[date]
    status:Optional[str]
