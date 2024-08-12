from app.schemas import TableQueryBody, Filter
from app.utils import filters_to_sqlalchemy
from typing import Dict, Annotated, Union
from fastapi import Query
from pydantic import  BaseModel
import json



def get_table_query_body(
        filters : Annotated[Union[str, None], Query()]= "{}", 
        skip: int = 0, limit: int = 10, 
        sort_by: str="updated_at", 
        sort_order :int = 1)-> TableQueryBody:
    filters : Dict[str, Filter] = json.loads(filters)
    tqb = TableQueryBody(filters=filters, skip=skip, limit=limit, 
                         sort_by=sort_by, sort_order=sort_order)
    return tqb