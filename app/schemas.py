from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class SavedIssueOut(BaseModel):
    id: int
    issue_key: str
    saved_at: datetime

    class Config:
        from_attributes = True

class SearchHistoryOut(BaseModel):
    id: int
    issue_key: str
    searched_at: datetime

    class Config:
        from_attributes = True
