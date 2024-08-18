
from app.models import BaseSQLModel
import pandas as pd
from typing import Optional, List
from sqlalchemy.orm import Session, Query, aliased
from sqlalchemy import select, Row, ColumnElement, \
ColumnExpressionArgument, ClauseElement, func, Select
from app.database import analysis_engine

class ETLPipeline:
    def __init__(self, model: BaseSQLModel, session: Session, query: Optional[Select] = None):
        self.model = model
        self.session = session
        self.query = query if query is not None else select(self.model)
        self.filters = []
        self.joins = []
        self.outerjoins = []
        self.order_bys = []
        self.group_bys = []
        self.havings = []
    # Extract Functions

    def set_extract_action(self, select_clauses: Optional[List[ClauseElement]] = [],
                           where_clauses: Optional[List[ColumnExpressionArgument]] = [
    ]):
        
        tmp_query = select(self.model)
        
        if len(select_clauses) > 0:
            tmp_query = select(*select_clauses)
      

        for clause in where_clauses:
            if clause is not None:
                self.filters.append(clause)
                tmp_query = tmp_query.where(clause)

        self.query = tmp_query

    # Transform Functions
    def add_query_filters(self, qfilters: List[ClauseElement] = []):
        for clause in qfilters:
            if clause is not None:
                self.filters.append(clause)
                self.query = self.query.where(clause)

    def set_order_attribute(self, sort_clause: ColumnElement):
        self.order_bys = [sort_clause]
        self.query = self.query.order_by(None).order_by(sort_clause)

    def append_order_attribute(self, sort_clause: ColumnElement):
        self.order_bys.append(sort_clause)
        self.query = self.query.order_by(sort_clause)

    def paginate_results(self, skip: int = 0, limit: int = 10):
        self.query = self.query.offset(skip).limit(limit)
    
    def join_on_model(self, join_clause, on_condition = None, left_join = False):
        if on_condition is not None:
            self.joins.append((join_clause, on_condition))
            self.query = self.query.join(join_clause, on_condition, isouter=left_join)
        else:
            self.joins.append((join_clause))
            self.query = self.query.join(join_clause, isouter=left_join)


    def outer_join_on_model(self, join_clause, on_condition = None):
        if on_condition is not None:
            self.outerjoins.append(join_clause, on_condition)
            self.query = self.query.outerjoin(join_clause, on_condition)
        else:
            self.outerjoins.append(join_clause, on_condition)
            self.query = self.query.outerjoin(join_clause)

    def group_by(self, group_clause):
        #Agg functions need to be in select clause or all select fields must be in group
        self.group_bys.append(group_clause)
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


class PandasAnalyzer(ETLPipeline):
    def from_db_to_pd(self, query,params) -> pd.DataFrame:        
        df = pd.read_sql(query, self.session.bind, params=params)    
        return df
    def export_excel_file(self, table_query:str, cyclic_count_id: str) :
        df = self.from_db_to_pd(query=table_query,params=(cyclic_count_id,))
        df.to_excel("test_output.xlsx")
    def excel_to_df(self):
        pass