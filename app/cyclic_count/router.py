from io import BytesIO
from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session
from uuid import UUID
from app.auth.models import User
from app.inventory.models import Warehouse
from app.service import ResourceRouter
from app.auth.middleware import current_user
from . import schemas, service
from .models import CyclicCount, CountRegistry, ActivityRegistry
from ..database import get_session
import aiofiles
import pandas as pd
router = APIRouter(tags=["Cyclic Count Module"])

cyclic_count_related = {
    "warehouses": Warehouse,
}
cyclic_count_m2m_keys = {
    "warehouse_ids": "warehouses",
}

class LogTracedRouter(ResourceRouter):
    def create(self):
        @self.router.post(f"/{self.name}/", response_model=self.detailed_schema)
        def get_create_route(resource: self.create_schema,
            session: Session = Depends(get_session), 
            user: User = Depends(current_user)):
            return self.model_repo.create_resource(session=session, resource=resource, user=user)
    def update(self):
        @self.router.put(f"/{self.name}/"+"{resource_id}", response_model=self.detailed_schema)
        def get_update_route(resource: self.update_schema,
                            resource_id: UUID,
                            session: Session = Depends(get_session),
                            user: User = Depends(current_user)):
            return self.model_repo.update_resource(session=session, resource_id=resource_id, resource=resource, user=user)
    def delete(self):
        @self.router.delete(f"/{self.name}/"+"{resource_id}", response_model=self.read_schema)
        def get_delete_route(resource_id: UUID,
            session: Session = Depends(get_session), 
            user: User = Depends(current_user)):
            return self.model_repo.delete_resource(session=session, resource_id=resource_id, user=user)


ccount_router = LogTracedRouter(model=CyclicCount, name="cyclic_counts",
                               model_repo=service.cyclic_count_crud,
                               read_schema=schemas.ReadCyclicCount,
                               detailed_schema=schemas.DetailedCyclicCount,
                               create_schema=schemas.CreateCyclicCount,
                               update_schema=schemas.UpdateCyclicCount,
                               related_dict=cyclic_count_related,
                               related_ids_dict=cyclic_count_m2m_keys
                               )
cregistry_router = LogTracedRouter(model=CountRegistry, name="count_registries",
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


@router.get("/cyclic_counts/{cyclic_count_id}/file", response_model=schemas.DetailedCyclicCount)
def get_cyclic_count_file(cyclic_count_id: UUID, db: Session = Depends(get_session)):
    return service.export_cyclic_count(db, cyclic_count_id=cyclic_count_id)


@router.post("/cyclic_counts/{cyclic_count_id}/upload")
async def upload(cyclic_count_id: UUID, file: UploadFile = File(...), db: Session = Depends(get_session)):
    try:
        async with aiofiles.open(file.filename, 'wb') as f:
            while contents := await file.read(1024 * 1024):
                await f.write(contents)
            
                data = BytesIO(contents)
                df = pd.read_excel(data, engine="openpyxl")
                
                test_result = service.create_products_from_file(db=db, cyclic_count_id=cyclic_count_id
                                                                ,dataframe=df)
                print("COMPLETED FILE UPLOAD :D")
                return {"message": "Succesful Upload" if test_result.status == 200 else "Found some errors on file",
                        **test_result.model_dump()
                        }
                
    except Exception as e:
        print(str(e))
        return {"message": f"There was an error uploading the file {e}"}
    finally:
        await file.close()


@router.post("/cyclic_counts/{cyclic_count_id}/upload/test")
async def test_file(cyclic_count_id: UUID,file: UploadFile = File(...), db: Session = Depends(get_session)):
    try:
        async with aiofiles.open(file.filename, 'wb') as f:
            while contents := await file.read(1024 * 1024):
                await f.write(contents)
            
                data = BytesIO(contents)
                df = pd.read_excel(data, engine="openpyxl")
                
                test_result = service.test_models_creation(db=db, dataframe=df)
                print("COMPLETED FILE UPLOAD :D")
                return {"message": "Succesful Upload" if test_result.status == 200 else "Found some errors on file",
                        **test_result.model_dump()
                        }
                
    except Exception as e:
        print(str(e))
        return {"message": f"There was an error uploading the file {e}"}
    finally:
        await file.close()

    




router.include_router(ccount_router.get_crud_routes())
router.include_router(cregistry_router.get_crud_routes())
router.include_router(aregistry_router.get_crud_routes())
