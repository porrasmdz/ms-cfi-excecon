from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from . import schemas, services, models
from ..database import get_db

router = APIRouter()

### CYCLIC_COUNT ROUTES ##########

@router.get("/cyclic_counts/", response_model=List[schemas.ReadCyclicCount])
def read_cyclic_counts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return services.get_cyclic_counts(db, skip=skip, limit=limit)

@router.post("/cyclic_counts/", response_model=schemas.ReadCyclicCount)
def create_cyclic_count(cyclic_count: schemas.CreateCyclicCount, db: Session = Depends(get_db)):
    return services.create_cyclic_count(db, cyclic_count=cyclic_count)

@router.get("/cyclic_counts/{cyclic_count_id}", response_model=schemas.ReadCyclicCount)
def read_cyclic_count(cyclic_count_id: UUID, db: Session = Depends(get_db)):
    return services.get_cyclic_count(db, cyclic_count_id=cyclic_count_id)

@router.put("/cyclic_counts/{cyclic_count_id}", response_model=schemas.ReadCyclicCount)
def update_cyclic_count(cyclic_count_id: UUID, cyclic_count: schemas.UpdateCyclicCount, db: Session = Depends(get_db)):
    return services.update_cyclic_count(db, cyclic_count_id=cyclic_count_id, cyclic_count=cyclic_count)

@router.delete("/cyclic_counts/{cyclic_count_id}", response_model=schemas.ReadCyclicCount)
def delete_cyclic_count(cyclic_count_id: UUID, db: Session = Depends(get_db)):
    return services.delete_cyclic_count(db, cyclic_count_id=cyclic_count_id)

### COUNT_REGISTRY ROUTES ##########

@router.get("/count_registries/", response_model=List[schemas.ReadCountRegistry])
def read_count_registries(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return services.get_count_registries(db, skip=skip, limit=limit)

@router.post("/count_registries/", response_model=schemas.ReadCountRegistry)
def create_count_registry(count_registry: schemas.CreateCountRegistry, db: Session = Depends(get_db)):
    return services.create_count_registry(db, count_registry=count_registry)

@router.get("/count_registries/{count_registry_id}", response_model=schemas.ReadCountRegistry)
def read_count_registry(count_registry_id: UUID, db: Session = Depends(get_db)):
    return services.get_count_registry(db, count_registry_id=count_registry_id)

@router.put("/count_registries/{count_registry_id}", response_model=schemas.ReadCountRegistry)
def update_count_registry(count_registry_id: UUID, count_registry: schemas.UpdateCountRegistry, db: Session = Depends(get_db)):
    return services.update_count_registry(db, count_registry_id=count_registry_id, count_registry=count_registry)

@router.delete("/count_registries/{count_registry_id}", response_model=schemas.ReadCountRegistry)
def delete_count_registry(count_registry_id: UUID, db: Session = Depends(get_db)):
    return services.delete_count_registry(db, count_registry_id=count_registry_id)

### ACTIVITY_REGISTRY ROUTES ##########

@router.get("/activity_registries/", response_model=List[schemas.ReadActivityRegistry])
def read_activity_registries(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return services.get_activity_registries(db, skip=skip, limit=limit)

@router.post("/activity_registries/", response_model=schemas.ReadActivityRegistry)
def create_activity_registry(activity_registry: schemas.CreateActivityRegistry, db: Session = Depends(get_db)):
    return services.create_activity_registry(db, activity_registry=activity_registry)

@router.get("/activity_registries/{activity_registry_id}", response_model=schemas.ReadActivityRegistry)
def read_activity_registry(activity_registry_id: UUID, db: Session = Depends(get_db)):
    return services.get_activity_registry(db, activity_registry_id=activity_registry_id)

@router.put("/activity_registries/{activity_registry_id}", response_model=schemas.ReadActivityRegistry)
def update_activity_registry(activity_registry_id: UUID, activity_registry: schemas.UpdateActivityRegistry, db: Session = Depends(get_db)):
    return services.update_activity_registry(db, activity_registry_id=activity_registry_id, activity_registry=activity_registry)

@router.delete("/activity_registries/{activity_registry_id}", response_model=schemas.ReadActivityRegistry)
def delete_activity_registry(activity_registry_id: UUID, db: Session = Depends(get_db)):
    return services.delete_activity_registry(db, activity_registry_id=activity_registry_id)
