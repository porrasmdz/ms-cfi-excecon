from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import TypeAdapter
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, Query
from typing import Annotated, Dict, List, Any, Optional
# from app.constants import get_class_from_str
from app.database import get_session
from app.dependencies import get_table_query_body
from app.models import BaseSQLModel
from app.schemas import  CreateSchema, PaginatedResource, ReadSchema, TableQueryBody, UpdateSchema
from app.utils import filters_to_sqlalchemy, update_validating_deletion_time

def get_paginated_resource(model:BaseSQLModel, filters: List[Any], tqb: TableQueryBody, session: Session):
    skip = tqb.skip
    limit= tqb.limit
    sort_by= tqb.sort_by
    sort_order= tqb.sort_order
    table_query = session.query(model)
    #TODO Catch exceptions
    for filter in filters:
        if filter is not None:
            table_query = table_query.filter(filter)
    
    sort_attr = getattr(model, sort_by)
    if(sort_order == 1):
        table_query = table_query.order_by(sort_attr.asc())
    else:
        table_query = table_query.order_by(sort_attr.desc())
    totalResults = table_query.count()
    results = table_query.offset(skip).limit(limit).all()
    
    return (totalResults, results)


def create_related_fields(db: Session, model_dict: Dict[str, Any], lookup_key: str, lookup_class):
    resulting_models = []
    if lookup_key in model_dict.keys():
        if len(model_dict[lookup_key]) > 0:
            for wh_id in model_dict[lookup_key]:
                resource = db.query(lookup_class).filter(
                    lookup_class.id == wh_id).first()
                if resource is not None:
                    resulting_models.append(resource)
        model_dict.pop(lookup_key)
        return resulting_models
    return []


def paginate_aggregated_resource(query:Query, filters: List[Any], tqb: TableQueryBody):
    skip = tqb.skip
    limit= tqb.limit
    sort_by= tqb.sort_by
    sort_order= tqb.sort_order
    table_query = query
    #TODO Catch exceptions
    for filter in filters:
        if filter is not None:
            table_query = table_query.filter(filter)
    
    # sort_attr = getattr(table_query, sort_by)
    # if(sort_order == 1):
    #     table_query = table_query.order_by(sort_attr.asc())
    # else:
        # table_query = table_query.order_by(sort_attr.desc())
    totalResults = table_query.count()
    results = table_query.offset(skip).limit(limit).all()
    
    return (totalResults, results)



def get_relationship_filters(model, filters: Dict, related_dict: Dict[str, BaseSQLModel]):
    composed_filters = {key: filters[key]
                        for key in filters.keys() if "." in key}
    related_filters = []
    for attribute, filter in composed_filters.items():
        related_class = related_dict[attribute]
        attribute_class = attribute.split(".")[0]
        original_attr = getattr(model, attribute_class)
        related_filters.append(original_attr.any(
            related_class.id.in_([filter.value])))

    return related_filters

class DatabaseRepository:
    def __init__(self, model: BaseSQLModel,
                 related_models: Optional[Dict[str,BaseSQLModel]] = {},
                 related_keys: Optional[Dict[str, str]] = {}):
        self.model = model
        self.related_m2m_models = related_models
        self.related_m2m_keys = related_keys
        #check dependent attributes 
    def get_all_resources(self, session: Session, filters: List[Any], tqb: TableQueryBody):
        try:
            return get_paginated_resource(self.model, filters, tqb, session)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                                detail=f"Error desconocido {e}")
    def get_one_resource(self, session: Session, resource_id: UUID):
        result = session.query(self.model).filter(
        self.model.id == resource_id).first()
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Resource with id {resource_id} not found")
        return result
    def create_resource(self, session: Session, resource: CreateSchema):
        try:
            new_resource = {**resource.model_dump()}
            local_keys = [k for k in new_resource.keys()]
            for key in local_keys:
                if "_ids" in key:
                    
                    print("M2M Related key: ", key)
                    lookup_rel_key = key
                    new_resource[self.related_m2m_keys[lookup_rel_key]] = create_related_fields(
                        session, new_resource, lookup_rel_key, 
                        self.related_m2m_models[lookup_rel_key])
            session_resource = self.model(**new_resource)
            session.add(session_resource)
            session.commit()
            session.refresh(session_resource)
            return session_resource
        except IntegrityError as ie:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail=f"{ie.orig}")
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                                detail=f"Error desconocido {ie}")
    def update_resource(self, session: Session, resource_id: UUID, resource: UpdateSchema):
        session_resource =self.get_one_resource(resource_id=resource_id, session=session)
        edition_resource = resource.model_dump()
        for related_key in self.related_m2m_keys.keys():
            if related_key in edition_resource.keys() and edition_resource[related_key] is not None:
                related_model_key = self.related_m2m_keys[related_key]
                edition_resource[related_model_key] = create_related_fields(
                    session, edition_resource, related_key, self.related_m2m_models[related_key])

        for key, value in edition_resource.items():
            update_validating_deletion_time(session_resource, key, value)
        session.commit()
        session.refresh(session_resource)
        return session_resource
    
    def delete_resource(self, session: Session, resource_id: UUID):
        session_resource = self.get_one_resource(resource_id=resource_id, session=session)
        # if len(session_resource.dependent) > 0:
        #     raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
        #                         detail=f"Resource with id {resource_id} contains related models. Please delete all first.")
        #Iterate through dependent attrs and raise error if not empty
        session.delete(session_resource)
        session.commit()

        return session_resource

class ResourceRouter:
    def __init__(self, model: BaseSQLModel,
                 name:str, model_repo: DatabaseRepository, 
                 read_schema: ReadSchema, detailed_schema: ReadSchema,
                 create_schema: CreateSchema, update_schema: UpdateSchema,
                 related_dict: Optional[Dict[str, BaseSQLModel]] = {},
                 related_ids_dict: Optional[Dict[str, str]] = {}):
        self.name = name
        self.model = model
        self.model_repo =  model_repo
        self.router = APIRouter()
        self.read_schema =  read_schema
        self.detailed_schema = detailed_schema
        self.create_schema = create_schema
        self.update_schema = update_schema
        self.related_dict = related_dict
        self.related_ids_dict = related_ids_dict

    def get_all(self):
        @self.router.get(f"/{self.name}/", response_model=PaginatedResource[self.detailed_schema])
        def get_all_route(tqb: TableQueryBody = Depends(get_table_query_body),
            session: Session = Depends(get_session)):
            filters = filters_to_sqlalchemy(model=self.model, filters=tqb.filters)
            relationship_filter = get_relationship_filters(
                model=self.model, filters=tqb.filters, related_dict=self.related_dict)
            filters = filters + relationship_filter
            (total_results, results) = self.model_repo.get_all_resources(
                filters=filters, tqb=tqb, session=session)
            response_resource = PaginatedResource(totalResults=total_results, results=results,
                                                skip=tqb.skip, limit=tqb.limit)
            return response_resource
    def get_one(self):
        @self.router.get(f"/{self.name}/"+"{resource_id}", response_model=self.detailed_schema)
        def get_one_route(resource_id: UUID,
            session: Session = Depends(get_session)): 
            session_resource =  self.model_repo.get_one_resource(resource_id=resource_id, session=session) 
            final_resource = self.detailed_schema.model_validate(session_resource)
            final_resource = final_resource.model_dump()
            for related_key in self.related_ids_dict.keys():
                related_model_key = self.related_ids_dict[related_key]
                final_resource[related_key] = [item["id"] for item in final_resource[related_model_key]]
            final_resource = self.detailed_schema.model_validate(final_resource)            
            return final_resource         
    def create(self):
        @self.router.post(f"/{self.name}/", response_model=self.detailed_schema)
        def get_create_route(resource: self.create_schema,
            session: Session = Depends(get_session)):
            return self.model_repo.create_resource(session=session, resource=resource)

    def update(self):
        @self.router.put(f"/{self.name}/"+"{resource_id}", response_model=self.detailed_schema)
        def get_update_route(resource: self.update_schema,
                            resource_id: UUID,
                            session: Session = Depends(get_session)):
            return self.model_repo.update_resource(session=session, resource_id=resource_id, resource=resource)

    def delete(self):
        @self.router.delete(f"/{self.name}/"+"{resource_id}", response_model=self.read_schema)
        def get_delete_route(resource_id: UUID,
            session: Session = Depends(get_session)):
            return self.model_repo.delete_resource(session=session, resource_id=resource_id)
    def get_crud_routes(self) -> APIRouter:
        self.get_all()
        self.get_one()
        self.create()
        self.update()
        self.delete()
        return self.router
    