from sqlalchemy import ColumnElement
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from uuid import UUID
from typing import List, Any, Dict
from app.etl_pipelines.service import ETLPipeline
from app.inventory.schemas import UpdateProduct
from app.service import DatabaseRepository, create_related_fields, get_paginated_resource, paginate_aggregated_resource
from app.schemas import TableQueryBody, BaseSQLModel
from app.cyclic_count.models import CountRegistry, CyclicCount
from app.models import ccount_product_table
from app.utils import update_validating_deletion_time
from .models import (
    Warehouse, WarehouseType, WHLocation, WHLocation_Type,
    Product, ProductCategory, MeasureUnit
)

from datetime import datetime


# CRUD Operations for Warehouse
warehouse_crud = DatabaseRepository(
    model=Warehouse 
)
# CRUD Operations for WarehouseType
whtype_crud = DatabaseRepository(
    model= WarehouseType
)

whlocation_crud = DatabaseRepository(
    model= WHLocation
)
whlocation_types_crud = DatabaseRepository(
    model= WHLocation_Type
)
product_category_crud = DatabaseRepository(
    model= ProductCategory
)
measure_unit_crud = DatabaseRepository(
    model= MeasureUnit
)


# CRUD Operations for Product
# TODO: Check MeasureUnits, ProductCategory, Warehouses, Warehouse Locations exist
products_m2m_models = {
    "warehouse_ids": Warehouse,
    "cyclic_count_ids": CyclicCount,
    "whlocation_ids": WHLocation
    }
products_m2m_keys = {
    "warehouse_ids": "warehouses",
    "cyclic_count_ids": "cyclic_counts",
    "whlocation_ids": "warehouse_locations"
    }
products_crud = DatabaseRepository(model=Product, 
                                   related_keys=products_m2m_keys,
                                   related_models=products_m2m_models)

def get_cyclic_count_nested_products(session: Session, 
                                     filters: list, 
                                     skip: int, limit: int, 
                                     sort_by: ColumnElement, 
                                     sort_order: int,
                                     cyclic_count_id: str):
    ppipeline = ETLPipeline(model=Product, session=session)
    ppipeline.add_query_filters(filters)
    ppipeline.add_query_filters([Product.cyclic_counts.any(CyclicCount.id == cyclic_count_id)])
    if sort_order == 1:
        ppipeline.set_order_attribute(sort_by.asc())
    else:
        ppipeline.set_order_attribute(sort_by.desc())
    total_results = ppipeline.get_pipeline_results_count()
    ppipeline.paginate_results(skip=skip, limit=limit)
    
    results = ppipeline.execute_pipeline()
    return (total_results, results)


