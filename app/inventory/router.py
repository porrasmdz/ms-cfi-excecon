from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from typing import Dict
from app.schemas import PaginatedResource, TableQueryBody
from app.dependencies import get_table_query_body
from app.utils import filters_to_sqlalchemy
from .models import Warehouse, WarehouseType, WHLocation, WHLocation_Type, Product, ProductCategory, MeasureUnit
from .models import CyclicCount
from . import service, schemas
from ..database import get_session


def get_class_from_str(key: str):
    match key:
        case "cyclic_counts":
            return CyclicCount
        case _:
            return CyclicCount


def get_relationship_filters(model, filters: Dict):
    composed_filters = {key: filters[key]
                        for key in filters.keys() if "." in key}
    related_filters = []
    for attribute, filter in composed_filters.items():
        related_class = get_class_from_str(attribute)
        attribute_class = attribute.split(".")[0]
        original_attr = getattr(model, attribute_class)
        related_filters.append(original_attr.any(
            related_class.id.in_([filter.value])))

    return related_filters
    # if isComposed:
    #     related_class = field.property.instrument_class

    #     print("######################GOT", field, match_mode, value, related_class)
    #     return (field.has(field.id==value))


router = APIRouter()


@router.get("/warehouses/", response_model=PaginatedResource[schemas.DetailedWarehouse])
def read_warehouses(tqb: TableQueryBody = Depends(get_table_query_body),
                    session: Session = Depends(get_session)):
    filters = filters_to_sqlalchemy(model=Warehouse, filters=tqb.filters)
    (total_registries, registries) = service.get_warehouses(model=Warehouse, filters=filters,
                                                            tqb=tqb, session=session)
    response = PaginatedResource(totalResults=total_registries, results=registries,
                                 skip=tqb.skip, limit=tqb.limit)
    return response


@router.get("/warehouses/{warehouse_id}", response_model=schemas.DetailedWarehouse)
def read_warehouse(warehouse_id: UUID, session: Session = Depends(get_session)):
    session_warehouse = service.get_warehouse(
        session, warehouse_id=warehouse_id)
    if session_warehouse is None:
        raise HTTPException(status_code=404, detail="Warehouse not found")
    return session_warehouse


@router.post("/warehouses/", response_model=schemas.DetailedWarehouse)
def create_warehouse(warehouse: schemas.CreateWarehouse, session: Session = Depends(get_session)):
    return service.create_warehouse(session=session, warehouse=warehouse)


@router.put("/warehouses/{warehouse_id}", response_model=schemas.DetailedWarehouse)
def update_warehouse(warehouse_id: UUID, warehouse: schemas.UpdateWarehouse, session: Session = Depends(get_session)):
    return service.update_warehouse(session=session, warehouse_id=warehouse_id, warehouse=warehouse)


@router.delete("/warehouses/{warehouse_id}", response_model=schemas.ReadWarehouse)
def delete_warehouse(warehouse_id: UUID, session: Session = Depends(get_session)):
    return service.delete_warehouse(session=session, warehouse_id=warehouse_id)

# WarehouseType routes


@router.get("/warehouse_types/", response_model=PaginatedResource[schemas.ReadWarehouseType])
def read_warehouse_types(tqb: TableQueryBody = Depends(get_table_query_body),
                         session: Session = Depends(get_session)):
    filters = filters_to_sqlalchemy(model=WarehouseType, filters=tqb.filters)
    (total_registries, registries) = service.get_warehouse_types(model=WarehouseType, filters=filters,
                                                                 tqb=tqb, session=session)
    response = PaginatedResource(totalResults=total_registries, results=registries,
                                 skip=tqb.skip, limit=tqb.limit)
    return response


@router.get("/warehouse_types/{warehouse_type_id}", response_model=schemas.DetailedWarehouseType)
def read_warehouse_type(warehouse_type_id: UUID, session: Session = Depends(get_session)):
    session_warehouse_type = service.get_warehouse_type(
        session, warehouse_type_id=warehouse_type_id)
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


@router.get("/whlocations/", response_model=PaginatedResource[schemas.DetailedWHLocation])
def read_whlocations(tqb: TableQueryBody = Depends(get_table_query_body),
                     session: Session = Depends(get_session)):
    filters = filters_to_sqlalchemy(model=WHLocation, filters=tqb.filters)
    (total_registries, registries) = service.get_whlocations(model=WHLocation, filters=filters,
                                                             tqb=tqb, session=session)
    response = PaginatedResource(totalResults=total_registries, results=registries,
                                 skip=tqb.skip, limit=tqb.limit)
    return response


@router.get("/whlocations/{whlocation_id}", response_model=schemas.DetailedWHLocation)
def read_whlocation(whlocation_id: UUID, session: Session = Depends(get_session)):
    session_whlocation = service.get_whlocation(
        session, whlocation_id=whlocation_id)
    if session_whlocation is None:
        raise HTTPException(status_code=404, detail="WHLocation not found")
    return session_whlocation


@router.post("/whlocations/", response_model=schemas.DetailedWHLocation)
def create_whlocation(whlocation: schemas.CreateWHLocation, session: Session = Depends(get_session)):
    return service.create_whlocation(session=session, whlocation=whlocation)


@router.put("/whlocations/{whlocation_id}", response_model=schemas.DetailedWHLocation)
def update_whlocation(whlocation_id: UUID, whlocation: schemas.UpdateWHLocation, session: Session = Depends(get_session)):
    return service.update_whlocation(session=session, whlocation_id=whlocation_id, whlocation=whlocation)


@router.delete("/whlocations/{whlocation_id}", response_model=schemas.ReadWHLocation)
def delete_whlocation(whlocation_id: UUID, session: Session = Depends(get_session)):
    return service.delete_whlocation(session=session, whlocation_id=whlocation_id)


# WHLocation_Type routes
@router.get("/whlocation_types/", response_model=PaginatedResource[schemas.ReadWHLocationType])
def read_whlocation_types(tqb: TableQueryBody = Depends(get_table_query_body),
                          session: Session = Depends(get_session)):
    filters = filters_to_sqlalchemy(model=WHLocation_Type, filters=tqb.filters)
    (total_registries, registries) = service.get_whlocation_types(model=WHLocation_Type, filters=filters,
                                                                  tqb=tqb, session=session)
    response = PaginatedResource(totalResults=total_registries, results=registries,
                                 skip=tqb.skip, limit=tqb.limit)
    return response


@router.get("/whlocation_types/{whlocation_type_id}", response_model=schemas.ReadWHLocationType)
def read_whlocation_type(whlocation_type_id: UUID, session: Session = Depends(get_session)):
    session_whlocation_type = service.get_whlocation_type(
        session, whlocation_type_id=whlocation_type_id)
    if session_whlocation_type is None:
        raise HTTPException(
            status_code=404, detail="WHLocation_Type not found")
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


@router.get("/products/", response_model=PaginatedResource[schemas.DetailedProduct])
def read_products(tqb: TableQueryBody = Depends(get_table_query_body),
                  session: Session = Depends(get_session)):
    filters = filters_to_sqlalchemy(model=Product, filters=tqb.filters)
    relationship_filter = get_relationship_filters(
        model=Product, filters=tqb.filters)
    filters = filters + relationship_filter
    

    (total_registries, registries) = service.get_products(model=Product, filters=filters,
                                                          tqb=tqb, session=session)
    response = PaginatedResource(totalResults=total_registries, results=registries,
                                 skip=tqb.skip, limit=tqb.limit)
    return response


@router.get("/products/{product_id}", response_model=schemas.DetailedProduct)
def read_product(product_id: UUID, session: Session = Depends(get_session)):
    session_product = service.get_product(session, product_id=product_id)
    if session_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    final_product = schemas.DetailedProduct.model_validate(session_product)
    final_product.warehouse_ids = [wh.id for wh in final_product.warehouses]
    final_product.cyclic_count_ids = [
        wh.id for wh in final_product.cyclic_counts]
    final_product.whlocation_ids = [
        wh.id for wh in final_product.warehouse_locations]
    return final_product


@router.get("/cyclic_count/{cyclic_count_id}/products/", response_model=PaginatedResource[schemas.CountNestedProduct])
def read_nested_product( cyclic_count_id: UUID, tqb: TableQueryBody = Depends(get_table_query_body),
                        session: Session = Depends(get_session)):
    filters = filters_to_sqlalchemy(model=Product, filters=tqb.filters)
    relationship_filter = get_relationship_filters(
        model=Product, filters=tqb.filters)
    filters = filters + relationship_filter 
    sort_by= getattr(Product, tqb.sort_by)
    
    (total_registries, registries) = service \
    .get_cyclic_count_nested_products(
        session=session,
        filters=filters,
        skip=tqb.skip, 
        limit=tqb.limit, 
        sort_by=sort_by, 
        sort_order=tqb.sort_order,
        cyclic_count_id=str(cyclic_count_id))
   
    # (total_registries, registries) = service.get_nested_products(cyclic_count_id=cyclic_count_id, filters=filters,
                                                                #  tqb=tqb, session=session)
    for registry in registries:
        counts = [ ]
        for cregistry in registry.count_registries:
            if cregistry.cyclic_count_id == cyclic_count_id:
                counts.append(cregistry) 
        registry.count_registries = counts
    response = PaginatedResource(totalResults=total_registries, results=registries,
                                 skip=tqb.skip, limit=tqb.limit)
    return response
   


@router.post("/products/", response_model=schemas.DetailedProduct)
def create_product(product: schemas.CreateProduct, session: Session = Depends(get_session)):
    return service.create_product(session=session, product=product)


@router.put("/products/{product_id}", response_model=schemas.DetailedProduct)
def update_product(product_id: UUID, product: schemas.UpdateProduct, session: Session = Depends(get_session)):
    return service.update_product(session=session, product_id=product_id, product=product)


@router.delete("/products/{product_id}", response_model=schemas.ReadProduct)
def delete_product(product_id: UUID, session: Session = Depends(get_session)):
    return service.delete_product(session=session, product_id=product_id)

# ProductCategory routes


@router.get("/product_categories/", response_model=PaginatedResource[schemas.DetailedProductCategory])
def read_product_categories(tqb: TableQueryBody = Depends(get_table_query_body),
                            session: Session = Depends(get_session)):
    filters = filters_to_sqlalchemy(model=ProductCategory, filters=tqb.filters)
    (total_registries, registries) = service.get_product_categories(model=ProductCategory, filters=filters,
                                                                    tqb=tqb, session=session)
    response = PaginatedResource(totalResults=total_registries, results=registries,
                                 skip=tqb.skip, limit=tqb.limit)
    return response


@router.get("/product_categories/{product_category_id}", response_model=schemas.DetailedProductCategory)
def read_product_category(product_category_id: UUID, session: Session = Depends(get_session)):
    session_product_category = service.get_product_category(
        session, product_category_id=product_category_id)
    if session_product_category is None:
        raise HTTPException(
            status_code=404, detail="Product Category not found")
    return session_product_category


@router.post("/product_categories/", response_model=schemas.DetailedProductCategory)
def create_product_category(product_category: schemas.CreateProductCategory, session: Session = Depends(get_session)):
    return service.create_product_category(session=session, product_category=product_category)


@router.put("/product_categories/{product_category_id}", response_model=schemas.DetailedProductCategory)
def update_product_category(product_category_id: UUID, product_category: schemas.UpdateProductCategory, session: Session = Depends(get_session)):
    return service.update_product_category(session=session, product_category_id=product_category_id, product_category=product_category)


@router.delete("/product_categories/{product_category_id}", response_model=schemas.DetailedProductCategory)
def delete_product_category(product_category_id: UUID, session: Session = Depends(get_session)):
    return service.delete_product_category(session=session, product_category_id=product_category_id)

# MeasureUnit routes


@router.get("/measure_units/", response_model=PaginatedResource[schemas.DetailedMeasureUnit])
def read_measure_units(tqb: TableQueryBody = Depends(get_table_query_body),
                       session: Session = Depends(get_session)):
    filters = filters_to_sqlalchemy(model=MeasureUnit, filters=tqb.filters)
    (total_registries, registries) = service.get_measure_units(model=MeasureUnit, filters=filters,
                                                               tqb=tqb, session=session)
    response = PaginatedResource(totalResults=total_registries, results=registries,
                                 skip=tqb.skip, limit=tqb.limit)
    return response


@router.get("/measure_units/{measure_unit_id}", response_model=schemas.DetailedMeasureUnit)
def read_measure_unit(measure_unit_id: UUID, session: Session = Depends(get_session)):
    session_measure_unit = service.get_measure_unit(
        session, measure_unit_id=measure_unit_id)
    if session_measure_unit is None:
        raise HTTPException(status_code=404, detail="MeasureUnit not found")
    return session_measure_unit


@router.post("/measure_units/", response_model=schemas.DetailedMeasureUnit)
def create_measure_unit(measure_unit: schemas.CreateMeasureUnit, session: Session = Depends(get_session)):
    return service.create_measure_unit(session=session, measure_unit=measure_unit)


@router.put("/measure_units/{measure_unit_id}", response_model=schemas.DetailedMeasureUnit)
def update_measure_unit(measure_unit_id: UUID, measure_unit: schemas.UpdateMeasureUnit, session: Session = Depends(get_session)):
    return service.update_measure_unit(session=session, measure_unit_id=measure_unit_id, measure_unit=measure_unit)


@router.delete("/measure_units/{measure_unit_id}", response_model=schemas.DetailedMeasureUnit)
def delete_measure_unit(measure_unit_id: UUID, session: Session = Depends(get_session)):
    return service.delete_measure_unit(session=session, measure_unit_id=measure_unit_id)
