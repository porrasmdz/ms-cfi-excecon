from app.schemas import TableQueryBody, Filter
from app.utils import filters_to_sqlalchemy
from typing import Dict


def get_table_query_body(filters : Dict[str, Filter]={}, skip: int = 0, limit: int = 10, 
                           sort_by: str="updated_at", sort_order :int = 1)-> TableQueryBody:
    tqb = TableQueryBody(filters=filters, skip=skip, limit=limit, 
                         sort_by=sort_by, sort_order=sort_order)
    return tqb