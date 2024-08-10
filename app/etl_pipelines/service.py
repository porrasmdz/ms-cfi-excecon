
from app.models import BaseSQLModel
from typing import Optional, List
from sqlalchemy.orm import Session, Query, aliased
from sqlalchemy import select, Row, ColumnElement, \
ColumnExpressionArgument, ClauseElement, func


class ETLPipeline:
    def __init__(self, model: BaseSQLModel, session: Session, query: Optional[Query] = None):
        self.model = model
        self.session = session
        self.query = select(query) if query is not None else select(self.model)
    # Extract Functions

    def set_extract_action(self, select_clauses: Optional[List[ClauseElement]] = [],
                           where_clauses: Optional[List[ColumnExpressionArgument]] = [
    ]):
        
        print("####SETTING EXTRACT ACTION")
        tmp_query = select(self.model)
        
        if len(select_clauses) > 0:
            tmp_query = select(*select_clauses)
      

        print("####SET EXTRACT ACTION")
        for clause in where_clauses:
            if clause is not None:
                tmp_query = tmp_query.where(clause)

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
    
    def join_on_model(self, join_clause, on_condition = None, left_join = False):
        if on_condition is not None:
            self.query = self.query.join(join_clause, on_condition, isouter=left_join)
        else:
            self.query = self.query.join(join_clause, isouter=left_join)


    def outer_join_on_model(self, join_clause, on_condition = None):
        if on_condition is not None:
            self.query = self.query.outerjoin(join_clause, on_condition)
        else:
            self.query = self.query.outerjoin(join_clause)

    def group_by(self, group_clause):
        #Agg functions need to be in select clause or all select fields must be in group
        self.query = self.query.group_by(group_clause)

    # Load Functions
    def get_pipeline_results_count(self):
        subq = self.query.subquery()
        aliased_result = aliased(self.model, subq)
        final_query = select(aliased_result)
        total_results = self.session.scalar(
            select(func.count()).select_from(final_query))

        return total_results

    def execute_pipeline(self) -> List[BaseSQLModel]:
        # print("####EXECUTING QUERY", str(self.query))
        results_rows = self.session.execute(self.query).scalars().all()
        self.query = select(self.model)  # flush query pipeline
        return results_rows
    
    def execute_pipeline_rows(self) -> List[Row]:
        
        # print("####EXECUTING QUERY ROWS", str(self.query))
        results_rows = self.session.execute(self.query).all()
        self.query = select(self.model)  # flush query pipeline
        return results_rows


