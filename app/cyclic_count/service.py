from sqlalchemy.orm import Session, make_transient
from uuid import UUID
from fastapi import HTTPException
from typing import List, Any
from app.etl_pipelines.service import ETLPipeline
from app.schemas import TableQueryBody
from app.models import BaseSQLModel
from app.inventory.models import Warehouse
from app.service import DatabaseRepository, get_paginated_resource
from app.utils import get_next_ccount
from .models import (CyclicCount, CountRegistry, ActivityRegistry)

cyclic_count_m2m_models = {
    "warehouse_ids": Warehouse,
}
cyclic_count_m2m_keys = {
    "warehouse_ids": "warehouses",
}
cyclic_count_crud = DatabaseRepository(
    model=CyclicCount, related_keys=cyclic_count_m2m_keys, related_models=cyclic_count_m2m_models)
count_registry_crud = DatabaseRepository(model=CountRegistry)
activity_registry_crud = DatabaseRepository(model=ActivityRegistry)



def close_cyclic_count(db: Session, cyclic_count_id: UUID):
    # Copy ccount
    cyclic_count: CyclicCount = cyclic_count_crud.get_one_resource(session=db, resource_id=cyclic_count_id)
    db.expunge(cyclic_count)
    make_transient(cyclic_count)
    # Update new count values
    del cyclic_count.id
    previous_ccount: CyclicCount = cyclic_count_crud.get_one_resource(session=db, resource_id=cyclic_count_id)
    cyclic_count.previous_ccount = previous_ccount
    cyclic_count.count_type = get_next_ccount(cyclic_count.count_type)
    cyclic_count.warehouses = previous_ccount.warehouses

    # This work should be defered to a WORKER and use lazy dynamic to iterate through large list
    # First add m2m products then copy system registries from previous count WHERE DIFF != 0
    cyclic_count.products = previous_ccount.products

    registries_pipeline = ETLPipeline(model=CountRegistry, session=db)
    for product in cyclic_count.products:
        registries_pipeline.add_query_filters([CountRegistry.cyclic_count_id == cyclic_count_id,
                                               CountRegistry.registry_type == "system",
                                               CountRegistry.product_id == product.id])
        system_registry: List[CountRegistry] = registries_pipeline.execute_pipeline(
        )
        if len(system_registry) > 0:
            reg = system_registry[0]
            db.expunge(reg)
            make_transient(reg)
            del reg.id
            reg.cyclic_count = cyclic_count
            reg.product = product
            db.add(reg)
            db.commit()
            db.refresh(reg)

    # CreateNew
    db.add(cyclic_count)
    db.commit()
    db.refresh(cyclic_count)
    return cyclic_count

