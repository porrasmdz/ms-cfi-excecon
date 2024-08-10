from app.inventory.models import Product
from app.models import BaseSQLModel
from typing import Optional, List
from sqlalchemy.orm import Session, Query, aliased
from sqlalchemy import select, Row, ColumnElement, ColumnExpressionArgument, ClauseElement, func


class ETLPipeline:
    def __init__(self, model: BaseSQLModel, session: Session, query: Optional[Query] = None):
        self.model = model
        self.session = session
        self.query = select(query) if query is not None else select(self.model)
    # Extract Functions

    def set_extract_action(self, select_clause: Optional[ClauseElement] = None,
                           where_clauses: Optional[List[ColumnExpressionArgument]] = [
    ],
        sort_clause: Optional[ColumnElement] = None
    ):
        tmp_query = select(self.model)
        if select_clause is not None:
            tmp_query = select(select_clause)

        for clause in where_clauses:
            if clause is not None:
                tmp_query = tmp_query.where(clause)

        if sort_clause is not None:
            tmp_query = tmp_query.order_by(sort_clause)
        else:
            tmp_query = tmp_query.order_by(self.model.updated_at.desc())
        self.query = tmp_query

    # Transform Functions
    def add_query_filters(self, qfilters: List[ClauseElement] = []):
        for clause in qfilters:
            if clause is not None:
                self.query = self.query.where(clause)

    def set_order_attribute(self, sort_clause: ColumnElement):
        self.query = self.query.order_by(None).order_by(sort_clause)

    def append_order_attribute(self, sort_clause: ColumnElement):
        self.query = self.query.order_by(sort_clause)

    def paginate_results(self, skip: int = 0, limit: int = 10):
        self.query = self.query.offset(skip).limit(limit)

    # Load Functions
    def get_pipeline_results_count(self):
        subq = self.query.subquery()
        aliased_result = aliased(self.model, subq)
        final_query = select(aliased_result)
        total_results = self.session.scalar(
            select(func.count()).select_from(final_query))

        return total_results

    def execute_pipeline(self) -> List[Row]:
        results_rows = self.session.execute(self.query).scalars()
        self.query = select(self.model)  # flush query pipeline
        return results_rows


def get_cyclic_count_nested_products(session: Session, filters: list, 
                                     skip: int, limit: int, 
                                     sort_by: ColumnElement, sort_order: int):
    ppipeline = ETLPipeline(model=Product, session=session)
    ppipeline.set_extract_action(where_clauses=filters)
    if sort_order == 1:
        ppipeline.set_order_attribute(sort_by.asc())
    else:
        ppipeline.set_order_attribute(sort_by.desc())

    total_results = ppipeline.get_pipeline_results_count()
    ppipeline.paginate_results(skip=skip, limit=limit)

    results = ppipeline.execute_pipeline()
    return (total_results, results)
