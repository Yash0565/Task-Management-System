from pydantic import BaseModel
from typing import Optional
from datetime import date,time
class WorklogBase(BaseModel):
    task_id:str
    work_date:str
    time_spent:str
    