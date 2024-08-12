from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from uuid import UUID
from typing import Annotated, Dict
from app.schemas import PaginatedResource, TableQueryBody
from app.dependencies import get_table_query_body
from app.service import ResourceRouter, get_relationship_filters
from app.utils import filters_to_sqlalchemy
from app.auth.models import User
from .models import Warehouse, WarehouseType, WHLocation, WHLocation_Type, Product, ProductCategory, MeasureUnit
from .models import CyclicCount
from . import service, schemas
from ..database import get_session

# if isComposed:
#     related_class = field.property.instrument_class

#     print("######################GOT", field, match_mode, value, related_class)
#     return (field.has(field.id==value))


router = APIRouter(tags=["Inventory Module"])

warehouse_router = ResourceRouter(model=Warehouse, name="warehouses",
                                  model_repo=service.warehouse_crud, read_schema=schemas.ReadWarehouse,
                                  detailed_schema=schemas.DetailedWarehouse, create_schema=schemas.CreateWarehouse,
                                  update_schema=schemas.UpdateWarehouse)

whtype_router = ResourceRouter(model=WarehouseType, name="warehouse_types",
                               model_repo=service.whtype_crud, read_schema=schemas.ReadWarehouseType,
                               detailed_schema=schemas.DetailedWarehouseType, create_schema=schemas.CreateWarehouseType,
                               update_schema=schemas.UpdateWarehouseType)
whlocation_router = ResourceRouter(model=WHLocation, name="whlocations",
                                   model_repo=service.whlocation_crud,
                                   read_schema=schemas.ReadWHLocation,
                                   detailed_schema=schemas.DetailedWHLocation,
                                   create_schema=schemas.CreateWHLocation,
                                   update_schema=schemas.UpdateWHLocation
                                   )
whlocation_type_router = ResourceRouter(model=WHLocation_Type, name="whlocation_types",
                                        model_repo=service.whlocation_types_crud,
                                        read_schema=schemas.ReadWHLocationType,
                                        detailed_schema=schemas.ReadWHLocationType,
                                        create_schema=schemas.CreateWHLocationType,
                                        update_schema=schemas.UpdateWHLocationType
                                        )

pcategory_router = ResourceRouter(model=ProductCategory, name="product_categories",
                                  model_repo=service.product_category_crud,
                                  read_schema=schemas.ReadProductCategory,
                                  detailed_schema=schemas.DetailedProductCategory,
                                  create_schema=schemas.CreateProductCategory,
                                  update_schema=schemas.UpdateProductCategory
                                  )

munit_router = ResourceRouter(model=MeasureUnit, name="measure_units",
                              model_repo=service.measure_unit_crud,
                              read_schema=schemas.ReadMeasureUnit,
                              detailed_schema=schemas.DetailedMeasureUnit,
                              create_schema=schemas.CreateMeasureUnit,
                              update_schema=schemas.UpdateMeasureUnit
                              )
related_models = {"cyclic_counts": CyclicCount}
related_ids_dict = {"warehouse_ids": "warehouses",
                    "cyclic_count_idss": "cyclic_counts",
                    "whlocation_ids": "warehouse_locations"}
product_router = ResourceRouter(model=Product, name="products",
                                model_repo=service.products_crud, read_schema=schemas.ReadProduct,
                                detailed_schema=schemas.DetailedProduct, create_schema=schemas.CreateProduct,
                                update_schema=schemas.UpdateProduct, related_dict=related_models,
                                related_ids_dict=related_ids_dict)


@router.get("/cyclic_count/{cyclic_count_id}/products/", response_model=PaginatedResource[schemas.CountNestedProduct])
def read_nested_product(cyclic_count_id: UUID, tqb: TableQueryBody = Depends(get_table_query_body),
                        session: Session = Depends(get_session)):
    filters = filters_to_sqlalchemy(model=Product, filters=tqb.filters)
    relationship_filter = get_relationship_filters(
        model=Product, filters=tqb.filters)
    filters = filters + relationship_filter
    sort_by = getattr(Product, tqb.sort_by)

    (total_registries, registries) = service \
        .get_cyclic_count_nested_products(
        session=session,
        filters=filters,
        skip=tqb.skip,
        limit=tqb.limit,
        sort_by=sort_by,
        sort_order=tqb.sort_order,
        cyclic_count_id=str(cyclic_count_id))

    # (total_registries, registries) = service.ucts(cyclic_count_id=cyclic_count_id, filters=filters,
    #  tqb=tqb, session=session)
    for registry in registries:
        counts = []
        for cregistry in registry.count_registries:
            if cregistry.cyclic_count_id == cyclic_count_id:
                counts.append(cregistry)
        registry.count_registries = counts
    response = PaginatedResource(totalResults=total_registries, results=registries,
                                 skip=tqb.skip, limit=tqb.limit)
    return response


router.include_router(warehouse_router.get_crud_routes())
router.include_router(whtype_router.get_crud_routes())
router.include_router(whlocation_router.get_crud_routes())
router.include_router(whlocation_type_router.get_crud_routes())
router.include_router(product_router.get_crud_routes())
router.include_router(pcategory_router.get_crud_routes())
router.include_router(munit_router.get_crud_routes())
