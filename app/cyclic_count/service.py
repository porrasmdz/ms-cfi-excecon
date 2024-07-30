from sqlalchemy.orm import Session
from uuid import UUID
from fastapi import HTTPException
from typing import List, Any
from app.schemas import TableQueryBody
from app.models import BaseSQLModel
from app.inventory.models import Warehouse
from app.service import get_paginated_resource
from .models import (CyclicCount, CountRegistry, ActivityRegistry)

def update_validating_deletion_time(object, key, value):
    if value is not None and key != "deleted_at":
        setattr(object, key, value)
    if key == "deleted_at":
        setattr(object, key, value)


### CYCLIC_COUNT SERVICES ##########

def get_cyclic_counts(model:BaseSQLModel, filters: List[Any], tqb: TableQueryBody, session: Session):
    return get_paginated_resource(model, filters, tqb, session)

def create_cyclic_count(db: Session, cyclic_count: CyclicCount):
    cyclic_dict ={**cyclic_count.model_dump()}
    cyclic_dict["warehouses"] = []
    if "warehouse_ids" in cyclic_dict.keys():
        if len(cyclic_dict["warehouse_ids"]) > 0:  
            for wh_id in cyclic_dict["warehouse_ids"]:
                warehouse = db.query(Warehouse).filter(Warehouse.id == wh_id).first()
                if warehouse is not None:
                    cyclic_dict["warehouses"].append(warehouse)
        cyclic_dict.pop("warehouse_ids")

    db_cyclic_count = CyclicCount(**cyclic_dict)
    db.add(db_cyclic_count)
    db.commit()
    db.refresh(db_cyclic_count)
    return db_cyclic_count

def get_cyclic_count(db: Session, cyclic_count_id: UUID):
    db_cyclic_count = db.query(CyclicCount).filter(CyclicCount.id == cyclic_count_id).first()
    if db_cyclic_count is None:
        raise HTTPException(status_code=404, detail="CyclicCount not found")
    return db_cyclic_count

def update_cyclic_count(db: Session, cyclic_count_id: UUID, cyclic_count: CyclicCount):
    cyclic_dict ={**cyclic_count.model_dump(exclude_unset=True)}
    if "warehouse_ids" in cyclic_dict.keys():
        if len(cyclic_dict["warehouse_ids"]) > 0:  
            
            cyclic_dict["warehouses"] = []
            for wh_id in cyclic_dict["warehouse_ids"]:
                warehouse = db.query(Warehouse).filter(Warehouse.id == wh_id).first()
                if warehouse is not None:
                    cyclic_dict["warehouses"].append(warehouse)
        else:
            cyclic_dict["warehouses"] = []
        cyclic_dict.pop("warehouse_ids")
        
    db_cyclic_count = db.query(CyclicCount).filter(CyclicCount.id == cyclic_count_id).first()
    if db_cyclic_count is None:
        raise HTTPException(status_code=404, detail="CyclicCount not found")
    
    for key, value in cyclic_dict.items():
        setattr(db_cyclic_count, key, value)
    db.commit()
    db.refresh(db_cyclic_count)
    return db_cyclic_count

def delete_cyclic_count(db: Session, cyclic_count_id: UUID):
    db_cyclic_count = db.query(CyclicCount).filter(CyclicCount.id == cyclic_count_id).first()
    if db_cyclic_count is None:
        raise HTTPException(status_code=404, detail="CyclicCount not found")
    db.delete(db_cyclic_count)
    db.commit()
    return db_cyclic_count

### COUNT_REGISTRY SERVICES ##########

def get_count_registries(model:BaseSQLModel, filters: List[Any], tqb: TableQueryBody, session: Session):
    return get_paginated_resource(model, filters, tqb, session)

def create_count_registry(db: Session, count_registry: CountRegistry):
    db_count_registry = CountRegistry(**count_registry.model_dump())
    db.add(db_count_registry)
    db.commit()
    db.refresh(db_count_registry)
    return db_count_registry

def get_count_registry(db: Session, count_registry_id: UUID):
    db_count_registry = db.query(CountRegistry).filter(CountRegistry.id == count_registry_id).first()
    if db_count_registry is None:
        raise HTTPException(status_code=404, detail="CountRegistry not found")
    return db_count_registry

def update_count_registry(db: Session, count_registry_id: UUID, count_registry: CountRegistry):
    db_count_registry = db.query(CountRegistry).filter(CountRegistry.id == count_registry_id).first()
    if db_count_registry is None:
        raise HTTPException(status_code=404, detail="CountRegistry not found")
    for key, value in count_registry.model_dump(exclude_unset=True).items():
        setattr(db_count_registry, key, value)
    db.commit()
    db.refresh(db_count_registry)
    return db_count_registry

def delete_count_registry(db: Session, count_registry_id: UUID):
    db_count_registry = db.query(CountRegistry).filter(CountRegistry.id == count_registry_id).first()
    if db_count_registry is None:
        raise HTTPException(status_code=404, detail="CountRegistry not found")
    db.delete(db_count_registry)
    db.commit()
    return db_count_registry

### ACTIVITY_REGISTRY SERVICES ##########

def get_activity_registries(model:BaseSQLModel, filters: List[Any], tqb: TableQueryBody, session: Session):
    return get_paginated_resource(model, filters, tqb, session)

def create_activity_registry(db: Session, activity_registry: ActivityRegistry):
    db_activity_registry = ActivityRegistry(**activity_registry.model_dump())
    db.add(db_activity_registry)
    db.commit()
    db.refresh(db_activity_registry)
    return db_activity_registry

def get_activity_registry(db: Session, activity_registry_id: UUID):
    db_activity_registry = db.query(ActivityRegistry).filter(ActivityRegistry.id == activity_registry_id).first()
    if db_activity_registry is None:
        raise HTTPException(status_code=404, detail="ActivityRegistry not found")
    return db_activity_registry

def update_activity_registry(db: Session, activity_registry_id: UUID, activity_registry: ActivityRegistry):
    db_activity_registry = db.query(ActivityRegistry).filter(ActivityRegistry.id == activity_registry_id).first()
    if db_activity_registry is None:
        raise HTTPException(status_code=404, detail="ActivityRegistry not found")
    for key, value in activity_registry.model_dump(exclude_unset=True).items():
        setattr(db_activity_registry, key, value)
    db.commit()
    db.refresh(db_activity_registry)
    return db_activity_registry

def delete_activity_registry(db: Session, activity_registry_id: UUID):
    db_activity_registry = db.query(ActivityRegistry).filter(ActivityRegistry.id == activity_registry_id).first()
    if db_activity_registry is None:
        raise HTTPException(status_code=404, detail="ActivityRegistry not found")
    db.delete(db_activity_registry)
    db.commit()
    return db_activity_registry