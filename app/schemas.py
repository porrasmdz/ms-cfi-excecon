from pydantic import BaseModel, PastDatetime, Field
from uuid import UUID
from typing import Optional
from datetime import datetime

class ReadSchema(BaseModel):
    id : UUID
    is_archived : bool
    created_at : PastDatetime 
    updated_at : PastDatetime
    deleted_at : Optional[PastDatetime]
    class Config:
        orm_mode = True

class CreateSchema(BaseModel):
    is_archived : Optional[bool] = Field(default=False)
    created_at : Optional[datetime] = Field(default_factory=datetime.now) 
    updated_at : Optional[datetime] = Field(default_factory=datetime.now)
    deleted_at : Optional[PastDatetime] = None
    class Config:   
        orm_mode = True

class UpdateSchema(BaseModel):
    is_archived : Optional[bool] = None
    deleted_at : Optional[PastDatetime] = None
    class Config:
        orm_mode = True