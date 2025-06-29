# ✅ Task Management Application

A backend task management system built for organizations to manage employee tasks with fine-grained access control using **Role-Based Access Control (RBAC)**.

---

## 🚀 Features

- 👥 Role-Based Access Control (Admin, User)
- ✅ Create, assign, and track tasks
- 📋 Employee-specific task views
- 🔐 Secure authentication using JWT
- 🗂️ Task status tracking (Pending, In Progress, Completed)
- 🕒 Deadlines and timestamps using `datetime`

---

## 🛠️ Tech Stack

- **Framework**: FastAPI
- **ORM**: SQLAlchemy
- **Authentication**: `python-jose`, `passlib` for hashing
- **Data Validation**: Pydantic
- **Other Libraries**: `datetime`

---

## 📦 Installation

> Make sure Python 3.8+ is installed

## Installing dependencies 

- pip install fastapi
- pip install uvicorn
- pip install sqlalchemy
- pip install python-jose
- pip install passlib[bcrypt]
- pip install pydantic 


## Running the Application 

- uvicorn main:app --reload


