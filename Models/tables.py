from sqlalchemy import create_engine, Column, Integer, String,Text,Enum, DATETIME, ForeignKey, DATE, TIME, VARCHAR, INT
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from datetime import date,time,datetime
from sqlalchemy.sql import func
from sqlalchemy import Enum as SqlEnum
import time
from enum import Enum as PyEnum

class Base(DeclarativeBase):
    pass

## Enum function for the values of "role" column in the users table
class RoleEnum(PyEnum):
    Admin = "Admin"
    User = "User"

## Enum function for the values of "status" column in the users table
class StatusEnum(PyEnum):
    Active = "Active"
    Inactive = "Inactive"

## Enum function for the values of "status" column in the tasks table
class taskStatusEnum(PyEnum):
    Pending="Pending"
    In_Process="In Process"
    Completed="Completed"

## Structure for the table 'users'
class User(Base):
    __tablename__="users"
    __allow_unmapped__ = True
    user_id=Column(VARCHAR(5),primary_key=True)
    name=Column(VARCHAR(50),nullable=False)
    password=Column(Text,nullable=False)
    mobile=Column(VARCHAR(10),nullable=False)
    email=Column(VARCHAR(30),nullable=False)
    role = Column(SqlEnum(RoleEnum), nullable=False)
    status = Column(SqlEnum(StatusEnum), nullable=False)
    created_at=Column(DATETIME(timezone=True),nullable=False,server_default=func.now())
    updated_at=Column(DATETIME(timezone=True),nullable=False,onupdate=func.now())

    # Relationships
    assigned_tasks = relationship("Task", back_populates="assigner", foreign_keys='Task.assignedBy')
    received_tasks = relationship("Task", back_populates="assignee", foreign_keys='Task.assignedTo')
    worklogs = relationship("WorkLog", back_populates="user")


## Structure for the table 'tasks'
class Task(Base):
    __tablename__="tasks"
    __allow_unmapped__ = True
    task_id=Column(VARCHAR(5),primary_key=True)
    task_name=Column(VARCHAR(50),nullable=False)
    desc=Column(Text,nullable=False)
    assignedBy = Column(String(5), ForeignKey('users.user_id')) 
    assignedTo = Column(String(5), ForeignKey('users.user_id'))
    due_date=Column(DATE,nullable=False)
    status=Column(SqlEnum(taskStatusEnum), nullable=False)
    task_created_at=Column(DATETIME(timezone=True),nullable=False,server_default=func.now())
    task_updated_at=Column(DATETIME(timezone=True),nullable=False,onupdate=func.now())

    # Relationships
    assigner = relationship("User", back_populates="assigned_tasks", foreign_keys=[assignedBy])
    assignee = relationship("User", back_populates="received_tasks", foreign_keys=[assignedTo])
    worklogs = relationship("WorkLog", back_populates="task")


## Structure for the table 'worklog'
class WorkLog(Base):
    __tablename__="worklog"
    __allow_unmapped__ = True
    work_id=Column(VARCHAR(5),primary_key=True)
    user_id=Column(String(5), ForeignKey('users.user_id'))
    task_id=Column(String(5), ForeignKey('tasks.task_id'))
    work_date=Column(DATE,nullable=False)
    time_spent=Column(TIME,nullable=False)
    created_at=Column(DATETIME,nullable=False)

    # Relationships
    user = relationship("User", back_populates="worklogs")
    task = relationship("Task", back_populates="worklogs")


    

