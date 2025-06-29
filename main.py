from fastapi import FastAPI
from User import user_routes 
from Task import task_routes
from Worklog import worklog_routes
from Models.database import Base, engine
from Report import report_routes
app = FastAPI() 

Base.metadata.create_all(bind=engine)

## USER MANAGEMENT APIs
app.include_router(user_routes.router2)
app.include_router(user_routes.router)

## Task MANAGEMENT APIs
app.include_router(task_routes.router)

## WORKLOG MANAGEMENT APIs
app.include_router(worklog_routes.router)

## REPORT MANAGEMENT APIs
app.include_router(report_routes.router)