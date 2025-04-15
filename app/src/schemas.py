from pydantic import BaseModel, Field, EmailStr
from typing import Literal

class BusinessAdd(BaseModel):
    name: str = Field(...)
    description: str = Field(...)
    location: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)

class BusinessEdit(BaseModel):
    name: str = Field(default=None)
    description: str = Field(default=None)
    location: str = Field(default=None)
    email: EmailStr = Field(default=None)
    password: str = Field(default=None)

class BusinessLogin(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

class ClientsEdit(BaseModel):
    name: str = Field(...)
    email: EmailStr = Field(...)
    location: str = Field(...)
    gender: Literal["male", "female", "unknown"] = Field(...)
    password: str = Field(...)
    age: int = Field(...)

class ClientsLogin(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

class ProgramAdd(BaseModel):
    name: str = Field(...)
    type: Literal["reward", "discount"] = Field(...)
    target: int = Field(default=None, ge=0)
    points_per_activation: int = Field(default=1, ge=0)
    reward: str = Field(...)
    max_claims: int = Field(..., ge=0)
    
class ProgramEdit(BaseModel):
    name: str = Field(default=None)
    target: int = Field(default=None, ge=0)
    reward: str = Field(default=None)
    points_per_activation: int = Field(default=None, ge=0)
    max_claims: int = Field(default=None, ge=0)