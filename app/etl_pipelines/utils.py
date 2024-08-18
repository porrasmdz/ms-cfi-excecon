from uuid import UUID
import numpy as np
from pandas import DataFrame
from sqlalchemy.orm import Session
from app.models import BaseSQLModel
from app.service import DatabaseRepository, locate_resource_from_name

def strip_whitespace_in_df(dataframe:DataFrame) -> DataFrame:
    df = dataframe
    for column in df:
        if df[column].dtype == "object":
            df[column] = df[column].str.strip()
    return df

def standarize_nulls_from_df(dataframe: DataFrame) -> DataFrame:
    df = strip_whitespace_in_df(dataframe=dataframe)            
    df = df.replace("",None)
    df = df.replace(np.nan,None)
    return df


def locate_null_rows_in_df(df:DataFrame, column_tag:str):
    null_mask = df[column_tag].isnull()
    null_rows = df[null_mask].values.tolist()
    null_indexes = (df.index[null_mask] + 2).to_list()
    
    return (null_indexes,null_rows)

def get_rows_w_nf_models_from_serie(db: Session, ref_model: BaseSQLModel,
                          res_crud: DatabaseRepository, df:DataFrame, 
                          serie_tag:str) -> list:
    serie = df[serie_tag].unique()
    models_lookup = [model for model in serie if model is not None]
    notfounds = []
    def locate_res(name:str):
        return locate_resource_from_name(
            db=db, model=ref_model,
            res_crud=res_crud, name=name
        )
    for mod in models_lookup:
        res_mod = locate_res(mod)
        if res_mod is None:
            notfounds.append(mod)
    nf_condition = df[serie_tag].isin(notfounds) 
    nfs = df[nf_condition].values.tolist()
    nfs_idx = (df.index[nf_condition] + 2).to_list()
    return (nfs_idx,nfs)


    