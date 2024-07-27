from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List, Any
from app.schemas import PaginatedResource, TableQueryBody
from app.dependencies import get_table_query_body
from app.utils import filters_to_sqlalchemy
from .models import Warehouse, WarehouseType, WHLocation, WHLocation_Type, Product, ProductCategory, MeasureUnit
from . import service, schemas
from ..database import get_session

router = APIRouter()
@router.get("/warehouses/", response_model=PaginatedResource[schemas.ReadWarehouse])
def read_warehouses(tqb: TableQueryBody = Depends(get_table_query_body), 
                   session: Session = Depends(get_session) ):
    filters = filters_to_sqlalchemy(model=Warehouse, filters=tqb.filters) 
    (total_registries, registries)= service.get_warehouses(model=Warehouse, filters=filters, 
                                                       tqb=tqb, session=session)
    response = PaginatedResource(totalResults=total_registries, results=registries, 
                                 skip= tqb.skip, limit=tqb.limit)
    return response

@router.get("/warehouses/{warehouse_id}", response_model=schemas.DetailedWarehouse)
def read_warehouse(warehouse_id: UUID, session: Session = Depends(get_session)):
    session_warehouse = service.get_warehouse(session, warehouse_id=warehouse_id)
    if session_warehouse is None:
        raise HTTPException(status_code=404, detail="Warehouse not found")
    return session_warehouse

@router.post("/warehouses/", response_model=schemas.ReadWarehouse)
def create_warehouse(warehouse: schemas.CreateWarehouse, session: Session = Depends(get_session)):
    return service.create_warehouse(session=session, warehouse=warehouse)

@router.put("/warehouses/{warehouse_id}", response_model=schemas.ReadWarehouse)
def update_warehouse(warehouse_id: UUID, warehouse: schemas.UpdateWarehouse, session: Session = Depends(get_session)):
    return service.update_warehouse(session=session, warehouse_id=warehouse_id, warehouse=warehouse)

@router.delete("/warehouses/{warehouse_id}", response_model=schemas.ReadWarehouse)
def delete_warehouse(warehouse_id: UUID, session: Session = Depends(get_session)):
    return service.delete_warehouse(session=session, warehouse_id=warehouse_id)

# WarehouseType routes
@router.get("/warehouse_types/", response_model=PaginatedResource[schemas.ReadWarehouseType])
def read_warehouse_types(tqb: TableQueryBody = Depends(get_table_query_body), 
                   session: Session = Depends(get_session) ):
    filters = filters_to_sqlalchemy(model=WarehouseType, filters=tqb.filters) 
    (total_registries, registries)= service.get_warehouse_types(model=WarehouseType, filters=filters, 
                                                       tqb=tqb, session=session)
    response = PaginatedResource(totalResults=total_registries, results=registries, 
                                 skip= tqb.skip, limit=tqb.limit)
    return response

@router.get("/warehouse_types/{warehouse_type_id}", response_model=schemas.DetailedWarehouseType)
def read_warehouse_type(warehouse_type_id: UUID, session: Session = Depends(get_session)):
    session_warehouse_type = service.get_warehouse_type(session, warehouse_type_id=warehouse_type_id)
    if session_warehouse_type is None:
        raise HTTPException(status_code=404, detail="WarehouseType not found")
    return session_warehouse_type

@router.post("/warehouse_types/", response_model=schemas.ReadWarehouseType)
def create_warehouse_type(warehouse_type: schemas.CreateWarehouseType, session: Session = Depends(get_session)):
    return service.create_warehouse_type(session=session, warehouse_type=warehouse_type)

@router.put("/warehouse_types/{warehouse_type_id}", response_model=schemas.ReadWarehouseType)
def update_warehouse_type(warehouse_type_id: UUID, warehouse_type: schemas.UpdateWarehouseType, session: Session = Depends(get_session)):
    return service.update_warehouse_type(session=session, warehouse_type_id=warehouse_type_id, warehouse_type=warehouse_type)

@router.delete("/warehouse_types/{warehouse_type_id}", response_model=schemas.ReadWarehouseType)
def delete_warehouse_type(warehouse_type_id: UUID, session: Session = Depends(get_session)):
    return service.delete_warehouse_type(session=session, warehouse_type_id=warehouse_type_id)

# WHLocation routes
@router.get("/whlocations/", response_model=PaginatedResource[schemas.ReadWHLocation])
def read_whlocations(tqb: TableQueryBody = Depends(get_table_query_body), 
                   session: Session = Depends(get_session) ):
    filters = filters_to_sqlalchemy(model=WHLocation, filters=tqb.filters) 
    (total_registries, registries)= service.get_whlocations(model=WHLocation, filters=filters, 
                                                       tqb=tqb, session=session)
    response = PaginatedResource(totalResults=total_registries, results=registries, 
                                 skip= tqb.skip, limit=tqb.limit)
    return response

@router.get("/whlocations/{whlocation_id}", response_model=schemas.ReadWHLocation)
def read_whlocation(whlocation_id: UUID, session: Session = Depends(get_session)):
    session_whlocation = service.get_whlocation(session, whlocation_id=whlocation_id)
    if session_whlocation is None:
        raise HTTPException(status_code=404, detail="WHLocation not found")
    return session_whlocation

@router.post("/whlocations/", response_model=schemas.ReadWHLocation)
def create_whlocation(whlocation: schemas.CreateWHLocation, session: Session = Depends(get_session)):
    return service.create_whlocation(session=session, whlocation=whlocation)

@router.put("/whlocations/{whlocation_id}", response_model=schemas.ReadWHLocation)
def update_whlocation(whlocation_id: UUID, whlocation: schemas.UpdateWHLocation, session: Session = Depends(get_session)):
    return service.update_whlocation(session=session, whlocation_id=whlocation_id, whlocation=whlocation)

@router.delete("/whlocations/{whlocation_id}", response_model=schemas.ReadWHLocation)
def delete_whlocation(whlocation_id: UUID, session: Session = Depends(get_session)):
    return service.delete_whlocation(session=session, whlocation_id=whlocation_id)


# WHLocation_Type routes
@router.get("/whlocation_types/", response_model=PaginatedResource[schemas.ReadWHLocationType])
def read_whlocation_types(tqb: TableQueryBody = Depends(get_table_query_body), 
                   session: Session = Depends(get_session) ):
    filters = filters_to_sqlalchemy(model=WHLocation_Type, filters=tqb.filters) 
    (total_registries, registries)= service.get_whlocation_types(model=WHLocation_Type, filters=filters, 
                                                       tqb=tqb, session=session)
    response = PaginatedResource(totalResults=total_registries, results=registries, 
                                 skip= tqb.skip, limit=tqb.limit)
    return response

@router.get("/whlocation_types/{whlocation_type_id}", response_model=schemas.ReadWHLocationType)
def read_whlocation_type(whlocation_type_id: UUID, session: Session = Depends(get_session)):
    session_whlocation_type = service.get_whlocation_type(session, whlocation_type_id=whlocation_type_id)
    if session_whlocation_type is None:
        raise HTTPException(status_code=404, detail="WHLocation_Type not found")
    return session_whlocation_type

@router.post("/whlocation_types/", response_model=schemas.ReadWHLocationType)
def create_whlocation_type(whlocation_type: schemas.CreateWHLocationType, session: Session = Depends(get_session)):
    return service.create_whlocation_type(session=session, whlocation_type=whlocation_type)

@router.put("/whlocation_types/{whlocation_type_id}", response_model=schemas.ReadWHLocationType)
def update_whlocation_type(whlocation_type_id: UUID, whlocation_type: schemas.UpdateWHLocationType, session: Session = Depends(get_session)):
    return service.update_whlocation_type(session=session, whlocation_type_id=whlocation_type_id, whlocation_type=whlocation_type)

@router.delete("/whlocation_types/{whlocation_type_id}", response_model=schemas.ReadWHLocationType)
def delete_whlocation_type(whlocation_type_id: UUID, session: Session = Depends(get_session)):
    return service.delete_whlocation_type(session=session, whlocation_type_id=whlocation_type_id)

# Product routes
@router.get("/products/", response_model=PaginatedResource[schemas.ReadProduct])
def read_products(tqb: TableQueryBody = Depends(get_table_query_body), 
                   session: Session = Depends(get_session) ):
    filters = filters_to_sqlalchemy(model=Product, filters=tqb.filters) 
    (total_registries, registries)= service.get_products(model=Product, filters=filters, 
                                                       tqb=tqb, session=session)
    response = PaginatedResource(totalResults=total_registries, results=registries, 
                                 skip= tqb.skip, limit=tqb.limit)
    return response

@router.get("/products/{product_id}", response_model=schemas.ReadProduct)
def read_product(product_id: UUID, session: Session = Depends(get_session)):
    session_product = service.get_product(session, product_id=product_id)
    if session_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return session_product

@router.post("/products/", response_model=schemas.ReadProduct)
def create_product(product: schemas.CreateProduct, session: Session = Depends(get_session)):
    return service.create_product(session=session, product=product)

@router.put("/products/{product_id}", response_model=schemas.ReadProduct)
def update_product(product_id: UUID, product: schemas.UpdateProduct, session: Session = Depends(get_session)):
    return service.update_product(session=session, product_id=product_id, product=product)

@router.delete("/products/{product_id}", response_model=schemas.ReadProduct)
def delete_product(product_id: UUID, session: Session = Depends(get_session)):
    return service.delete_product(session=session, product_id=product_id)

# ProductCategory routes
@router.get("/product_categories/", response_model=PaginatedResource[schemas.ReadProductCategory])
def read_product_categories(tqb: TableQueryBody = Depends(get_table_query_body), 
                   session: Session = Depends(get_session) ):
    filters = filters_to_sqlalchemy(model=ProductCategory, filters=tqb.filters) 
    (total_registries, registries)= service.get_product_categories(model=ProductCategory, filters=filters, 
                                                       tqb=tqb, session=session)
    response = PaginatedResource(totalResults=total_registries, results=registries, 
                                 skip= tqb.skip, limit=tqb.limit)
    return response

@router.get("/product_categories/{product_category_id}", response_model=schemas.ReadProductCategory)
def read_product_category(product_category_id: UUID, session: Session = Depends(get_session)):
    session_product_category = service.get_product_category(session, product_category_id=product_category_id)
    if session_product_category is None:
        raise HTTPException(status_code=404, detail="Product Category not found")
    return session_product_category

@router.post("/product_categories/", response_model=schemas.ReadProductCategory)
def create_product_category(product_category: schemas.CreateProductCategory, session: Session = Depends(get_session)):
    return service.create_product_category(session=session, product_category=product_category)

@router.put("/product_categories/{product_category_id}", response_model=schemas.ReadProductCategory)
def update_product_category(product_category_id: UUID, product_category: schemas.UpdateProductCategory, session: Session = Depends(get_session)):
    return service.update_product_category(session=session, product_category_id=product_category_id, product_category=product_category)

@router.delete("/product_categories/{product_category_id}", response_model=schemas.ReadProductCategory)
def delete_product_category(product_category_id: UUID, session: Session = Depends(get_session)):
    return service.delete_product_category(session=session, product_category_id=product_category_id)

# MeasureUnit routes
@router.get("/measure_units/", response_model=PaginatedResource[schemas.ReadMeasureUnit])
def read_measure_units(tqb: TableQueryBody = Depends(get_table_query_body), 
                   session: Session = Depends(get_session) ):
    filters = filters_to_sqlalchemy(model=MeasureUnit, filters=tqb.filters) 
    (total_registries, registries)= service.get_measure_units(model=MeasureUnit, filters=filters, 
                                                       tqb=tqb, session=session)
    response = PaginatedResource(totalResults=total_registries, results=registries, 
                                 skip= tqb.skip, limit=tqb.limit)
    return response

@router.get("/measure_units/{measure_unit_id}", response_model=schemas.ReadMeasureUnit)
def read_measure_unit(measure_unit_id: UUID, session: Session = Depends(get_session)):
    session_measure_unit = service.get_measure_unit(session, measure_unit_id=measure_unit_id)
    if session_measure_unit is None:
        raise HTTPException(status_code=404, detail="MeasureUnit not found")
    return session_measure_unit

@router.post("/measure_units/", response_model=schemas.ReadMeasureUnit)
def create_measure_unit(measure_unit: schemas.CreateMeasureUnit, session: Session = Depends(get_session)):
    return service.create_measure_unit(session=session, measure_unit=measure_unit)

@router.put("/measure_units/{measure_unit_id}", response_model=schemas.ReadMeasureUnit)
def update_measure_unit(measure_unit_id: UUID, measure_unit: schemas.UpdateMeasureUnit, session: Session = Depends(get_session)):
    return service.update_measure_unit(session=session, measure_unit_id=measure_unit_id, measure_unit=measure_unit)

@router.delete("/measure_units/{measure_unit_id}", response_model=schemas.ReadMeasureUnit)
def delete_measure_unit(measure_unit_id: UUID, session: Session = Depends(get_session)):
    return service.delete_measure_unit(session=session, measure_unit_id=measure_unit_id)
