from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from Models.tables import Base

# Engine that connects to the database
engine = create_engine('sqlite:///project.db', connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# The base class for all models
Base = declarative_base()

def get_db():
    db = SessionLocal()  # Create a new session instance
    try:
        yield db
    finally:
        db.close()

