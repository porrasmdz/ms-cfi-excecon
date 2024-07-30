from typing import Optional, List, Literal
from pydantic import EmailStr, Field
from uuid import UUID
from datetime import date, datetime
from ..schemas import CreateSchema, ReadSchema, UpdateSchema
from app.inventory.schemas import ReadWarehouse , CreateWarehouse

###CYCLIC_COUNT##########
class ReadCyclicCount(ReadSchema):
    id: UUID
    name: str
    status: Optional[str] = "Abierto"
    count_type: str = "Primer Conteo"
    count_date_start: datetime = Field(default_factory=datetime.now)
    count_date_finish: datetime = Field(default_factory=datetime.now)

    warehouses: Optional[List["ReadWarehouse"]] 
    parent_id: Optional[UUID] = None
    
class CreateCyclicCount(CreateSchema):
    name: str
    status: Optional[str] = "Abierto"
    count_type: str = "Primer Conteo"
    count_date_start: datetime = Field(default_factory=datetime.now)
    count_date_finish: datetime = Field(default_factory=datetime.now)
    warehouse_ids: List["UUID"]
    parent_id: Optional[UUID] = None
    
class UpdateCyclicCount(UpdateSchema):
    name: Optional[str] = None
    status: Optional[str] = None 
    count_type: Optional[str] = None 
    count_date_start: Optional[datetime] = None
    count_date_finish: Optional[datetime] = None

    warehouse_ids: Optional[List["UUID"]] = None
    parent_id: Optional[UUID] = None
    
###COUNT_REGISTRY
class ReadCountRegistry(ReadSchema):
    id: UUID
    registry_type: Literal["system", "physical", "consolidated"]
    registry_units: int
    registry_cost: int
    difference_units: int
    difference_cost: int

    product_id: UUID
    cyclic_count_id: UUID

    
    

class CreateCountRegistry(CreateSchema):
    registry_type: Literal["system", "physical", "consolidated"]
    registry_units: int
    registry_cost: int
    difference_units: int
    difference_cost: int

    product_id: UUID
    cyclic_count_id: UUID

    
class UpdateCountRegistry(UpdateSchema):
    registry_type: Optional[Literal["system", "physical", "consolidated"]] = None
    registry_units: Optional[int] = None
    registry_cost: Optional[int] = None
    difference_units: Optional[int] = None
    difference_cost: Optional[int] = None

    product_id: Optional[UUID] = None
    cyclic_count_id: Optional[UUID] = None

    

###ACTIVITY_REGISTRY##############
class ReadActivityRegistry(ReadSchema):
    id: UUID
    detail: str
    commentary: str
    user: UUID
    count_registry_id: UUID
    
class CreateActivityRegistry(CreateSchema):
    detail: str
    commentary: Optional[str]
    user: UUID
    count_registry_id: UUID
    
class UpdateActivityRegistry(UpdateSchema):
    detail: Optional[str] = None
    commentary: Optional[str] = None
    user: Optional[UUID] = None
    count_registry_id: Optional[UUID] = None
