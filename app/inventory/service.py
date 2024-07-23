from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from uuid import UUID

from .models import (
    Warehouse, WarehouseType, WHLocation, WHLocation_Type,
    Product, ProductCategory, MeasureUnit
)

from datetime import datetime

def update_validating_deletion_time(object, key, value):
    if value is not None and key != "deleted_at":
        setattr(object, key, value)
    if key == "deleted_at":
        setattr(object, key, value)

def get_wh_locations_for_warehouse(db: Session, warehouse_id: UUID):
    warehouse = db.query(Warehouse).filter(Warehouse.id == warehouse_id).first()
    if warehouse:
        result = [wh_loc.id for wh_loc in warehouse.wh_locations]
        return result
    return []

# CRUD Operations for Warehouse
#TODO: Validate Company, Warehouse_Type exist
def get_warehouses(session: Session, skip: int = 0, limit: int = 100):
    wh_list = session.query(Warehouse).offset(skip).limit(limit).all()
    return wh_list

def get_warehouse(session: Session, warehouse_id: UUID):
    warehouse = session.query(Warehouse).filter(Warehouse.id == warehouse_id).first()
    
    return warehouse

def create_warehouse(session: Session, warehouse: Warehouse):
    session_warehouse = Warehouse(**warehouse.model_dump())
    session.add(session_warehouse)
    session.commit()
    session.refresh(session_warehouse)
    return session_warehouse

def update_warehouse(session: Session, warehouse_id: UUID, warehouse: Warehouse):
    session_warehouse = session.query(Warehouse).filter(Warehouse.id == warehouse_id).first()
    if session_warehouse:
        for key, value in warehouse.model_dump().items():
            update_validating_deletion_time(session_warehouse, key, value)
        session.commit()
        session.refresh(session_warehouse)
    else:
        raise HTTPException(status_code=400, detail=f"Warehouse with id {warehouse_id} not found")
    return session_warehouse

def delete_warehouse(session: Session, warehouse_id: UUID):
    session_warehouse = session.query(Warehouse).filter(Warehouse.id == warehouse_id).first()
    
    if not session_warehouse:
        raise HTTPException(status_code=400, detail=f"Warehouse with id {warehouse_id} not found")
    if len(session_warehouse.wh_locations) > 0:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail=f"Warehouse with id {warehouse_id} contains warehouse locations. Please delete all WH Locations first.")
    session.delete(session_warehouse)
    session.commit()
    return session_warehouse

# CRUD Operations for WarehouseType

def get_warehouse_types(session: Session, skip: int = 0, limit: int = 100):
    return session.query(WarehouseType).offset(skip).limit(limit).all()

def get_warehouse_type(session: Session, warehouse_type_id: UUID):
    return session.query(WarehouseType).filter(WarehouseType.id == warehouse_type_id).first()

def create_warehouse_type(session: Session, warehouse_type: WarehouseType):
    session_warehouse_type = WarehouseType(**warehouse_type.model_dump())
    session_warehouse_type.created_at = datetime.now()
    session_warehouse_type.updated_at = datetime.now()
    session.add(session_warehouse_type)
    session.commit()
    session.refresh(session_warehouse_type)
    return session_warehouse_type

def update_warehouse_type(session: Session, warehouse_type_id: UUID, warehouse_type: WarehouseType):
    session_warehouse_type = session.query(WarehouseType).filter(WarehouseType.id == warehouse_type_id).first()
    if session_warehouse_type:
        for key, value in warehouse_type.model_dump().items():
            update_validating_deletion_time(session_warehouse_type, key, value)
        session.commit()
        session.refresh(session_warehouse_type)
    else:
        raise HTTPException(status_code=400, detail=f"Warehouse Type with id {warehouse_type_id} not found")
    
    return session_warehouse_type

def delete_warehouse_type(session: Session, warehouse_type_id: UUID):
    session_warehouse_type = session.query(WarehouseType).filter(WarehouseType.id == warehouse_type_id).first()
    if session_warehouse_type:
        session.delete(session_warehouse_type)
        session.commit()
    else:
        raise HTTPException(status_code=400, detail=f"Warehouse Type with id {warehouse_type_id} not found")
    
    return session_warehouse_type

# CRUD Operations for WHLocation
#TODO: Check valid Warehouse_Location_Type, Parent_WHLocation, Warehouse exists

def get_whlocations(session: Session, skip: int = 0, limit: int = 100):
    return session.query(WHLocation).offset(skip).limit(limit).all()

def get_whlocation(session: Session, whlocation_id: UUID):
    return session.query(WHLocation).filter(WHLocation.id == whlocation_id).first()

def create_whlocation(session: Session, whlocation: WHLocation):
    session_whlocation = WHLocation(**whlocation.model_dump())
    session.add(session_whlocation)
    session.commit()
    session.refresh(session_whlocation)
    return session_whlocation

def update_whlocation(session: Session, whlocation_id: UUID, whlocation: WHLocation):
    session_whlocation = session.query(WHLocation).filter(WHLocation.id == whlocation_id).first()
    
    if session_whlocation:
        for key, value in whlocation.model_dump().items():
            update_validating_deletion_time(session_whlocation, key, value)
        session.commit()
        session.refresh(session_whlocation)

    else:
        raise HTTPException(status_code=400, detail=f"Warehouse Location with id {whlocation_id} not found")
    return session_whlocation

def delete_whlocation(session: Session, whlocation_id: UUID):
    session_whlocation = session.query(WHLocation).filter(WHLocation.id == whlocation_id).first()
    if session_whlocation:
        session.delete(session_whlocation)
        session.commit()
    else:
        raise HTTPException(status_code=400, detail=f"Warehouse Location with id {whlocation_id} not found")
    return session_whlocation

# CRUD Operations for WHLocation_Type

def get_whlocation_types(session: Session, skip: int = 0, limit: int = 100):
    return session.query(WHLocation_Type).offset(skip).limit(limit).all()

def get_whlocation_type(session: Session, whlocation_type_id: UUID):
    return session.query(WHLocation_Type).filter(WHLocation_Type.id == whlocation_type_id).first()

def create_whlocation_type(session: Session, whlocation_type: WHLocation_Type):
    session_whlocation_type = WHLocation_Type(**whlocation_type.model_dump())
    session.add(session_whlocation_type)
    session.commit()
    session.refresh(session_whlocation_type)
    return session_whlocation_type

def update_whlocation_type(session: Session, whlocation_type_id: UUID, whlocation_type: WHLocation_Type):
    session_whlocation_type = session.query(WHLocation_Type).filter(WHLocation_Type.id == whlocation_type_id).first()
    if session_whlocation_type:
        for key, value in whlocation_type.model_dump().items():
            update_validating_deletion_time(session_whlocation_type, key, value)
        session.commit()
        session.refresh(session_whlocation_type)
    else:
        raise HTTPException(status_code=400, detail=f"Warehouse Location Type with id {whlocation_type_id} not found")

    return session_whlocation_type

def delete_whlocation_type(session: Session, whlocation_type_id: UUID):
    session_whlocation_type = session.query(WHLocation_Type).filter(WHLocation_Type.id == whlocation_type_id).first()
    if session_whlocation_type:
        session.delete(session_whlocation_type)
        session.commit()
    else:
        raise HTTPException(status_code=400, detail=f"Warehouse Location Type with id {whlocation_type_id} not found")

    return session_whlocation_type

# CRUD Operations for Product
#TODO: Check MeasureUnits, ProductCategory, Warehouses, Warehouse Locations exist
def get_products(session: Session, skip: int = 0, limit: int = 100):
    return session.query(Product).offset(skip).limit(limit).all()

def get_product(session: Session, product_id: UUID):
    return session.query(Product).filter(Product.id == product_id).first()

def create_product(session: Session, product: Product):
    session_product = Product(**product.model_dump())
    session.add(session_product)
    session.commit()
    session.refresh(session_product)
    return session_product

def update_product(session: Session, product_id: UUID, product: Product):
    session_product = session.query(Product).filter(Product.id == product_id).first()
    if session_product:
        for key, value in product.model_dump().items():
            update_validating_deletion_time(session_product, key, value)
        session.commit()
        session.refresh(session_product)
    else:
        raise HTTPException(status_code=400, detail=f"Product with id {product_id} not found")

    return session_product

def delete_product(session: Session, product_id: UUID):
    session_product = session.query(Product).filter(Product.id == product_id).first()
    if session_product:
        session.delete(session_product)
        session.commit()
    else:
        raise HTTPException(status_code=400, detail=f"Product with id {product_id} not found")

    return session_product

# CRUD Operations for ProductCategory

def get_product_categories(session: Session, skip: int = 0, limit: int = 100):
    return session.query(ProductCategory).offset(skip).limit(limit).all()

def get_product_category(session: Session, product_category_id: UUID):
    return session.query(ProductCategory).filter(ProductCategory.id == product_category_id).first()

def create_product_category(session: Session, product_category: ProductCategory):
    session_product_category = ProductCategory(**product_category.model_dump())
    session.add(session_product_category)
    session.commit()
    session.refresh(session_product_category)
    return session_product_category

def update_product_category(session: Session, product_category_id: UUID, product_category: ProductCategory):
    session_product_category = session.query(ProductCategory).filter(ProductCategory.id == product_category_id).first()
    if session_product_category:
        for key, value in product_category.model_dump().items():
            update_validating_deletion_time(session_product_category, key, value)
        session.commit()
        session.refresh(session_product_category)
    else:
        raise HTTPException(status_code=400, detail=f"Product Category with id {product_category_id} not found")

    return session_product_category

def delete_product_category(session: Session, product_category_id: UUID):
    session_product_category = session.query(ProductCategory).filter(ProductCategory.id == product_category_id).first()
    if session_product_category:
        session.delete(session_product_category)
        session.commit()
    else:
        raise HTTPException(status_code=400, detail=f"Product Category with id {product_category_id} not found")

    return session_product_category

# CRUD Operations for MeasureUnit
#TODO: Check valid parent measure unit
def get_measure_units(session: Session, skip: int = 0, limit: int = 100):
    return session.query(MeasureUnit).offset(skip).limit(limit).all()

def get_measure_unit(session: Session, measure_unit_id: UUID):
    return session.query(MeasureUnit).filter(MeasureUnit.id == measure_unit_id).first()

def create_measure_unit(session: Session, measure_unit: MeasureUnit):
    session_measure_unit = MeasureUnit(**measure_unit.model_dump())
    session.add(session_measure_unit)
    session.commit()
    session.refresh(session_measure_unit)
    return session_measure_unit

def update_measure_unit(session: Session, measure_unit_id: UUID, measure_unit: MeasureUnit):
    session_measure_unit = session.query(MeasureUnit).filter(MeasureUnit.id == measure_unit_id).first()
    if session_measure_unit:
        for key, value in measure_unit.model_dump().items():
            update_validating_deletion_time(session_measure_unit, key, value)
        session.commit()
        session.refresh(session_measure_unit)
    else:
        raise HTTPException(status_code=400, detail=f"Measure Unit with id {measure_unit_id} not found")

    return session_measure_unit

def delete_measure_unit(session: Session, measure_unit_id: UUID):
    session_measure_unit = session.query(MeasureUnit).filter(MeasureUnit.id == measure_unit_id).first()
    if session_measure_unit:
        session.delete(session_measure_unit)
        session.commit()
        
    else:
        raise HTTPException(status_code=400, detail=f"Measure Unit with id {measure_unit_id} not found")

    return session_measure_unit
