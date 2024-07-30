from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from app.schemas import PaginatedResource, TableQueryBody
from app.dependencies import get_table_query_body
from app.utils import filters_to_sqlalchemy
from . import schemas, service
from .models import CyclicCount, CountRegistry, ActivityRegistry
from ..database import get_session

router = APIRouter()

### CYCLIC_COUNT ROUTES ##########

@router.get("/cyclic_counts/", response_model=PaginatedResource[schemas.ReadCyclicCount])
def read_cyclic_counts(tqb: TableQueryBody = Depends(get_table_query_body), 
                   session: Session = Depends(get_session) ):
    filters = filters_to_sqlalchemy(model=CyclicCount, filters=tqb.filters) 
    (total_ccounts, cyclic_counts)= service.get_cyclic_counts(model=CyclicCount, filters=filters, 
                                                       tqb=tqb, session=session)
    response = PaginatedResource(totalResults=total_ccounts, results=cyclic_counts, 
                                 skip= tqb.skip, limit=tqb.limit)
    return response

@router.post("/cyclic_counts/", response_model=schemas.ReadCyclicCount)
def create_cyclic_count(cyclic_count: schemas.CreateCyclicCount, db: Session = Depends(get_session)):
    return service.create_cyclic_count(db, cyclic_count=cyclic_count)

@router.get("/cyclic_counts/{cyclic_count_id}", response_model=schemas.ReadCyclicCount)
def read_cyclic_count(cyclic_count_id: UUID, db: Session = Depends(get_session)):
    return service.get_cyclic_count(db, cyclic_count_id=cyclic_count_id)

@router.put("/cyclic_counts/{cyclic_count_id}", response_model=schemas.ReadCyclicCount)
def update_cyclic_count(cyclic_count_id: UUID, cyclic_count: schemas.UpdateCyclicCount, db: Session = Depends(get_session)):
    return service.update_cyclic_count(db, cyclic_count_id=cyclic_count_id, cyclic_count=cyclic_count)

@router.delete("/cyclic_counts/{cyclic_count_id}", response_model=schemas.ReadCyclicCount)
def delete_cyclic_count(cyclic_count_id: UUID, db: Session = Depends(get_session)):
    return service.delete_cyclic_count(db, cyclic_count_id=cyclic_count_id)

### COUNT_REGISTRY ROUTES ##########

@router.get("/count_registries/", response_model=PaginatedResource[schemas.ReadCountRegistry])
def read_count_registries(tqb: TableQueryBody = Depends(get_table_query_body), 
                   session: Session = Depends(get_session) ):
    filters = filters_to_sqlalchemy(model=CountRegistry, filters=tqb.filters) 
    (total_cregistries, cregistries)= service.get_count_registries(model=CountRegistry, filters=filters, 
                                                       tqb=tqb, session=session)
    response = PaginatedResource(totalResults=total_cregistries, results=cregistries, 
                                 skip= tqb.skip, limit=tqb.limit)
    return response

@router.post("/count_registries/", response_model=schemas.ReadCountRegistry)
def create_count_registry(count_registry: schemas.CreateCountRegistry, db: Session = Depends(get_session)):
    print("RECEIVED CR",count_registry )
    return service.create_count_registry(db, count_registry=count_registry)

@router.get("/count_registries/{count_registry_id}", response_model=schemas.ReadCountRegistry)
def read_count_registry(count_registry_id: UUID, db: Session = Depends(get_session)):
    return service.get_count_registry(db, count_registry_id=count_registry_id)

@router.put("/count_registries/{count_registry_id}", response_model=schemas.ReadCountRegistry)
def update_count_registry(count_registry_id: UUID, count_registry: schemas.UpdateCountRegistry, db: Session = Depends(get_session)):
    return service.update_count_registry(db, count_registry_id=count_registry_id, count_registry=count_registry)

@router.delete("/count_registries/{count_registry_id}", response_model=schemas.ReadCountRegistry)
def delete_count_registry(count_registry_id: UUID, db: Session = Depends(get_session)):
    return service.delete_count_registry(db, count_registry_id=count_registry_id)

### ACTIVITY_REGISTRY ROUTES ##########

@router.get("/activity_registries/", response_model=PaginatedResource[schemas.ReadActivityRegistry])
def read_activity_registries(tqb: TableQueryBody = Depends(get_table_query_body), 
                   session: Session = Depends(get_session) ):
    filters = filters_to_sqlalchemy(model=ActivityRegistry, filters=tqb.filters) 
    (total_aregistries, activity_registries)= service.get_activity_registries(model=ActivityRegistry, filters=filters, 
                                                       tqb=tqb, session=session)
    response = PaginatedResource(totalResults=total_aregistries, results=activity_registries, 
                                 skip= tqb.skip, limit=tqb.limit)
    return response

@router.post("/activity_registries/", response_model=schemas.ReadActivityRegistry)
def create_activity_registry(activity_registry: schemas.CreateActivityRegistry, db: Session = Depends(get_session)):
    return service.create_activity_registry(db, activity_registry=activity_registry)

@router.get("/activity_registries/{activity_registry_id}", response_model=schemas.ReadActivityRegistry)
def read_activity_registry(activity_registry_id: UUID, db: Session = Depends(get_session)):
    return service.get_activity_registry(db, activity_registry_id=activity_registry_id)

@router.put("/activity_registries/{activity_registry_id}", response_model=schemas.ReadActivityRegistry)
def update_activity_registry(activity_registry_id: UUID, activity_registry: schemas.UpdateActivityRegistry, db: Session = Depends(get_session)):
    return service.update_activity_registry(db, activity_registry_id=activity_registry_id, activity_registry=activity_registry)

@router.delete("/activity_registries/{activity_registry_id}", response_model=schemas.ReadActivityRegistry)
def delete_activity_registry(activity_registry_id: UUID, db: Session = Depends(get_session)):
    return service.delete_activity_registry(db, activity_registry_id=activity_registry_id)
