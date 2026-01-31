from pydantic import BaseModel, Field, validator
from typing import Literal, Optional


class Profile(BaseModel):
    email: str
    phone: Optional[str] = None


class UserCreate(BaseModel):
    name: str
    role: Literal["admin", "manager", "team member"]
    profile: Profile

class UserResponse(BaseModel):
    id: int
    name: str
    role: str
    email: str
    phone: Optional[str]

    class Config:
        orm_mode = True  


class TaskCreate(BaseModel):
    title: str
    description: str
    priority: Literal["low", "medium", "high"]
    status: str
    assigned_to: Optional[int] = None

    @validator("title")
    def title_must_be_capitalized(cls, v):
        if not v[0].isupper():
            raise ValueError("Title must be capitalized")
        return v

class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    priority: str
    status: str
    assigned_to: Optional[int]

    class Config:
        orm_mode = True
