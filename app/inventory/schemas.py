from typing import Optional,  List
from pydantic import BaseModel
from uuid import UUID

from app.companies.schemas import ReadCompany
from ..schemas import CreateSchema, ReadSchema, UpdateSchema

###WAREHOUSES######
class ReadWarehouse(ReadSchema):
    id: UUID
    name: Optional[str] = None
    country: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None 
    company_id: UUID 
    warehouse_type_id: UUID

class DetailedWarehouse(ReadSchema):
    id: UUID
    name: Optional[str] = None
    country: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None 
    company_id: UUID 
    warehouse_type_id: UUID
    wh_locations: Optional[List["ReadWarehouseType"]]
    # company: "ReadCompany"
    warehouse_type: "ReadWarehouseType"


class CreateWarehouse(CreateSchema):
    name: Optional[str] = None
    country: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None 
    company_id: UUID 
    warehouse_type_id: UUID
class UpdateWarehouse(UpdateSchema):
    name: Optional[str] = None
    country: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None 
    company_id: Optional[UUID] = None  
    warehouse_type_id: Optional[UUID] = None 

###WH_TYPE##########
class ReadWarehouseType(ReadSchema):
    id: UUID
    name: str
    description: Optional[str] = None
class DetailedWarehouseType(ReadSchema):
    id: UUID
    name: str
    warehouses: Optional[List[ReadWarehouse]]
    description: Optional[str] = None

class CreateWarehouseType(CreateSchema):
    name: str
    description: Optional[str] = None

class UpdateWarehouseType(UpdateSchema):
    name: Optional[str] = None
    description: Optional[str] = None


###WH_LOCATION#########
class ReadWHLocation(ReadSchema):
    id: UUID
    name: str
    description: Optional[str] = None
    wh_location_type_id: Optional[UUID] = None
    parent_id: Optional[UUID] = None
    warehouse_id: UUID
    
class DetailedWHLocation(ReadSchema):
    id: UUID
    name: str
    description: Optional[str] = None
    wh_location_type: Optional["ReadWHLocationType"] = None
    parent_whlocation: Optional[ReadWHLocation] = None
    warehouse: ReadWarehouse
    warehouse_id: UUID
    parent_id: Optional[UUID] = None
    wh_location_type_id: Optional[UUID] = None
class CreateWHLocation(CreateSchema):
    name: str
    description: Optional[str] = None
    wh_location_type_id: Optional[UUID] = None
    parent_id: Optional[UUID] = None
    warehouse_id: UUID
class UpdateWHLocation(UpdateSchema):
    name: Optional[str] = None
    description: Optional[str] = None
    wh_location_type_id: Optional[UUID] = None
    parent_id: Optional[UUID] = None
    warehouse_id: Optional[UUID] = None

###WHLOCATION_TYPE#############
class ReadWHLocationType(ReadSchema):
    id: UUID
    name: str
class CreateWHLocationType(CreateSchema):
    name: str
class UpdateWHLocationType(UpdateSchema):
    name: Optional[str] = None

###PRODUCT_CATEGORY#######
class ReadProductCategory(ReadSchema):
    id: UUID
    name: str
    short_codename: str
    parent_id: Optional[UUID] = None
class DetailedProductCategory(ReadSchema):
    id: UUID
    name: str
    short_codename: str
    parent_category: Optional[ReadProductCategory] = None
    parent_id: Optional[UUID] = None
class CreateProductCategory(CreateSchema):
    name: str
    short_codename: str
class UpdateProductCategory(UpdateSchema):
    name: Optional[str]
    short_codename: Optional[str] = None


###MEASURE UNIT#######
class ReadMeasureUnit(ReadSchema):
    id: UUID
    name: str
    conversion_formula: Optional[str] = None
    parent_id: Optional[UUID] = None
    
class DetailedMeasureUnit(ReadSchema):
    id: UUID
    name: str
    conversion_formula: Optional[str] = None
    parent: Optional[ReadMeasureUnit] = None
    parent_id: Optional[UUID] = None


class CreateMeasureUnit(CreateSchema):
    name: str
    conversion_formula: Optional[str] = None
    parent_id: Optional[UUID] = None

class UpdateMeasureUnit(UpdateSchema):
    name: Optional[str] = None
    conversion_formula: Optional[str] = None
    parent_id: Optional[UUID] = None



###PRODUCT##########
class ReadProduct(ReadSchema):
    id: UUID
    name: str
    code: Optional[str] = None
    sku: Optional[str] = None
    unit_cost: int
    measure_unit_id: UUID
    category_id: UUID
class DetailedProduct(ReadSchema):
    id: UUID
    name: str
    code: Optional[str] = None
    sku: Optional[str] = None
    unit_cost: int
    measure_unit: ReadMeasureUnit
    category: ReadProductCategory
    measure_unit_id: UUID
    category_id: UUID

    warehouses: List[ReadWarehouse]
    warehouse_locations: Optional[List[ReadWHLocation]] = []
    cyclic_counts: List["ReadCyclicCount"] 

class CreateProduct(CreateSchema):
    name: str
    code: Optional[str] = None
    sku: Optional[str] = None
    unit_cost: int
    measure_unit_id: UUID
    category_id: UUID

    warehouse_ids: List["UUID"]
    whlocation_ids: List["UUID"] = []
    cyclic_count_ids: List["UUID"]

class UpdateProduct(UpdateSchema):
    name: Optional[str] = None
    code: Optional[str] = None
    sku: Optional[str] = None
    unit_cost: Optional[int] = None
    measure_unit_id: Optional[UUID] = None
    category_id: Optional[UUID] = None

    warehouse_ids: Optional[List["UUID"]] = None
    whlocation_ids: Optional[List["UUID"]] = None
    cyclic_count_ids: Optional[List["UUID"]] = None


from app.cyclic_count.schemas import ReadCyclicCount