from pydantic import BaseModel, EmailStr, validator
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    name: str
    email: EmailStr
    age: Optional[int] = None

    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Il nome non può essere vuoto')
        return v.strip()

    @validator('age')
    def age_must_be_positive(cls, v):
        if v is not None and v <= 0:
            raise ValueError('L\'età deve essere un numero positivo')
        return v

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    age: Optional[int] = None

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True