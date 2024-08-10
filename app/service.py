from sqlalchemy.orm import Session, Query
from typing import List, Any
from app.models import BaseSQLModel
from app.schemas import  TableQueryBody

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