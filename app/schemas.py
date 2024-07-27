from pydantic import BaseModel, PastDatetime, Field, ConfigDict
from uuid import UUID
from typing import Optional, Dict, Any, TypeVar, Generic, get_args, List
from app.models import BaseSQLModel
from enum import Enum
from datetime import datetime

class ReadSchema(BaseModel):
    id : UUID
    is_archived : bool
    created_at : PastDatetime 
    updated_at : PastDatetime
    deleted_at : Optional[PastDatetime]
    
    model_config = ConfigDict(from_attributes=True)

class CreateSchema(BaseModel):
    is_archived : Optional[bool] = Field(default=False)
    created_at : Optional[datetime] = Field(default_factory=datetime.now) 
    updated_at : Optional[datetime] = Field(default_factory=datetime.now)
    deleted_at : Optional[PastDatetime] = None

    model_config = ConfigDict(from_attributes=True)

class UpdateSchema(BaseModel):
    is_archived : Optional[bool] = None
    deleted_at : Optional[PastDatetime] = None
    
    model_config = ConfigDict(from_attributes=True)

class MatchMode(str, Enum):
    CONTAINS = "contains"
    NOT_CONTAINS = "notContains"
    IN = "in"
    LIKE = "like"

    EQUALS = "eq"
    NOT_EQUALS = "ne"
    GREATER_THAN="gt"
    LESS_THAN="lt"
    GREATER_EQUALS="ge"
    LESS_EQUALS="le"
    
    IS_EMPTY="isEmpty"
    IS_NOT_EMPTY="isNotEmpty"

class Filter(BaseModel):
    value: Optional[Any] = None
    match_mode: MatchMode

class TableQueryBody(BaseModel):
    filters: Dict[str, Filter] = {}
    skip: int = 0 #first
    limit: int = 10 #rows
    sort_by: Optional[str] = Field("updated_at")
    sort_order: Optional[int] = Field(1) #1 - ASC | 0 - DESC


T = TypeVar("T")
class PaginatedResource(BaseModel, Generic[T]):
    totalResults: int = 0
    results: List[T] = []
    skip: int = 0
    limit: int = 10