from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from app.utils import filters_to_sqlalchemy
from typing import List, Any
from app.dependencies import get_table_query_body
from app.schemas import TableQueryBody, PaginatedResource
from . import service
from ..database import get_session
from fastapi import APIRouter


router = APIRouter(tags=["ETL Module"])


# @router.get("/aggregation/", response_model=PaginatedResource[])
# def read_aggregation(tqb: TableQueryBody = Depends(get_table_query_body), 
#                    session: Session = Depends(get_session) ):    
#     filters = filters_to_sqlalchemy(model=Product, filters=tqb.filters) 
#     sort_by= getattr(Product, tqb.sort_by)
    
#     (total_results, results) = service \
#         .get_cyclic_count_nested_products(
#             session=session,
#             filters=filters,
#             skip=tqb.skip, 
#             limit=tqb.limit, 
#             sort_by=sort_by, 
#             sort_order=tqb.sort_order)
    
#     response_resource = PaginatedResource(totalResults=total_results, results=results, 
#                                  skip= tqb.skip, limit=tqb.limit)
    
#     return response_resource