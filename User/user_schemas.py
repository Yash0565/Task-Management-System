from pydantic import BaseModel, EmailStr
from typing import Optional , Literal
from enum import Enum

class RoleEnum(str, Enum):
    ADMIN = "Admin"
    USER = "User"

class StatusEnum(str, Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"

class UserBase(BaseModel):
    username:str
    password:str
    mobile:str
    email:EmailStr
    role: RoleEnum
    status: StatusEnum


class TokenRequest(BaseModel):
    userid: str
    password: str