from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from app.inventory.models import Warehouse
from app.schemas import PaginatedResource, TableQueryBody
from app.dependencies import get_table_query_body
from app.service import ResourceRouter
from app.utils import filters_to_sqlalchemy
from . import schemas, service
from .models import CyclicCount, CountRegistry, ActivityRegistry
from ..database import get_session

router = APIRouter(tags=["Cyclic Count Module"])

cyclic_count_related = {
    "warehouses": Warehouse,
}
cyclic_count_m2m_keys = {
    "warehouse_ids": "warehouses",
}
ccount_router = ResourceRouter(model=CyclicCount, name="cyclic_counts",
                               model_repo=service.cyclic_count_crud,
                               read_schema=schemas.ReadCyclicCount,
                               detailed_schema=schemas.DetailedCyclicCount,
                               create_schema=schemas.CreateCyclicCount,
                               update_schema=schemas.UpdateCyclicCount,
                               related_dict=cyclic_count_related,
                               related_ids_dict=cyclic_count_m2m_keys
                               )
cregistry_router = ResourceRouter(model=CountRegistry, name="count_registries",
                                  model_repo=service.count_registry_crud,
                                  read_schema=schemas.ReadCountRegistry,
                                  detailed_schema=schemas.DetailedCountRegistry,
                                  create_schema=schemas.CreateCountRegistry,
                                  update_schema=schemas.UpdateCountRegistry
                                  )
aregistry_router = ResourceRouter(model=ActivityRegistry, name="activity_registries",
                                  model_repo=service.activity_registry_crud,
                                  read_schema=schemas.ReadActivityRegistry,
                                  detailed_schema=schemas.DetailedActivityRegistry,
                                  create_schema=schemas.CreateActivityRegistry,
                                  update_schema=schemas.UpdateActivityRegistry
                                  )


@router.get("/cyclic_counts/{cyclic_count_id}/close", response_model=schemas.DetailedCyclicCount)
def close_cyclic_count(cyclic_count_id: UUID, db: Session = Depends(get_session)):
    return service.close_cyclic_count(db, cyclic_count_id=cyclic_count_id)


router.include_router(ccount_router.get_crud_routes())
router.include_router(cregistry_router.get_crud_routes())
router.include_router(aregistry_router.get_crud_routes())
