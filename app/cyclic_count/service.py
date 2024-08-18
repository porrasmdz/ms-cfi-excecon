from sqlalchemy.orm import Session, make_transient
from pandas import DataFrame
import numpy as np
from uuid import UUID
from typing import List
from app.cyclic_count.utils import create_test_response
from app.etl_pipelines.utils import get_rows_w_nf_models_from_serie, locate_null_rows_in_df, standarize_nulls_from_df
from app.etl_pipelines.service import ETLPipeline, PandasAnalyzer
from app.inventory.models import MeasureUnit, Warehouse,  ProductCategory
from app.inventory.service import measure_unit_crud, product_category_crud, products_crud
from app.inventory.schemas import CreateProduct
from app.service import DatabaseRepository, locate_resource_from_name
from .schemas import CreateCountRegistry
from app.utils import get_next_ccount
from .models import (CyclicCount, CountRegistry, ActivityRegistry)


cyclic_count_m2m_models = {
    "warehouse_ids": Warehouse,
}
cyclic_count_m2m_keys = {
    "warehouse_ids": "warehouses",
}
cyclic_count_crud = DatabaseRepository(
    model=CyclicCount, related_keys=cyclic_count_m2m_keys, related_models=cyclic_count_m2m_models)
count_registry_crud = DatabaseRepository(model=CountRegistry)
activity_registry_crud = DatabaseRepository(model=ActivityRegistry)


def test_models_creation(db: Session, dataframe: DataFrame):
    category_tag = "Categoria"
    mu_tag = "U.Medida"
    df = standarize_nulls_from_df(dataframe=dataframe)
    (null_cat_idxs, null_cat_rows) = locate_null_rows_in_df(df, category_tag)
    (null_mu_idxs, null_mu_rows) = locate_null_rows_in_df(df, mu_tag)

    (nf_cat_idxs, nf_cat_rows) = get_rows_w_nf_models_from_serie(db=db, ref_model=ProductCategory,
                                            res_crud=product_category_crud, df=df,
                                            serie_tag=category_tag)
    (nf_mu_idxs, nf_mu_rows) = get_rows_w_nf_models_from_serie(db=db, ref_model=MeasureUnit,
                                     res_crud=measure_unit_crud, df=df,
                                     serie_tag=mu_tag)
    result = create_test_response(
        null_cat_idx=null_cat_idxs, null_categories=null_cat_rows, nf_cat_idx=nf_cat_idxs, nf_cat_rows=nf_cat_rows,
        null_mu_idx=null_mu_idxs, null_mus=null_mu_rows, nf_mu_idx=nf_mu_idxs, nf_mu_rows=nf_mu_rows)
    return result


def close_cyclic_count(db: Session, cyclic_count_id: UUID):
    # Copy ccount
    cyclic_count: CyclicCount = cyclic_count_crud.get_one_resource(
        session=db, resource_id=cyclic_count_id)
    db.expunge(cyclic_count)
    make_transient(cyclic_count)
    # Update new count values
    del cyclic_count.id
    previous_ccount: CyclicCount = cyclic_count_crud.get_one_resource(
        session=db, resource_id=cyclic_count_id)
    cyclic_count.previous_ccount = previous_ccount
    cyclic_count.count_type = get_next_ccount(cyclic_count.count_type)
    cyclic_count.warehouses = previous_ccount.warehouses

    # This work should be defered to a WORKER and use lazy dynamic to iterate through large list
    # First add m2m products then copy system registries from previous count WHERE DIFF != 0
    cyclic_count.products = previous_ccount.products

    registries_pipeline = ETLPipeline(model=CountRegistry, session=db)
    for product in cyclic_count.products:
        registries_pipeline.add_query_filters([CountRegistry.cyclic_count_id == cyclic_count_id,
                                               CountRegistry.registry_type == "system",
                                               CountRegistry.product_id == product.id])
        system_registry: List[CountRegistry] = registries_pipeline.execute_pipeline(
        )
        if len(system_registry) > 0:
            reg = system_registry[0]
            db.expunge(reg)
            make_transient(reg)
            del reg.id
            reg.cyclic_count = cyclic_count
            reg.product = product
            db.add(reg)
            db.commit()
            db.refresh(reg)
    previous_ccount.status = "Cerrado"
    # CreateNew
    db.add(cyclic_count)
    db.commit()
    db.refresh(cyclic_count)
    return cyclic_count


def export_cyclic_count(db: Session, cyclic_count_id: UUID):
    # Copy ccount
    products_query = """SELECT ccnt.name AS ccount_name, p.code, p.sku, p.name, p.unit_cost, 
        mu.name AS mu_name, pc.name AS category_name, sr.registry_units AS system_units,
        sr.registry_cost AS system_cost, pr.registry_units AS physical_units, 
        pr.registry_cost AS physical_cost, (sr.registry_units - pr.registry_units) AS diff_units,
        (sr.registry_cost - pr.registry_cost) AS diff_cost
        FROM product AS p
    
        JOIN ccount_product_table AS ct ON p.id = product_id
        LEFT JOIN measure_unit AS mu ON p.measure_unit_id = mu.id
        LEFT JOIN product_category AS pc ON p.category_id = pc.id
        LEFT JOIN cyclic_count AS ccnt ON ccnt.id = ct.cyclic_count_id
        LEFT JOIN count_registry AS sr ON (sr.product_id = p.id AND sr.cyclic_count_id = ct.cyclic_count_id AND sr.registry_type = 'system')
        LEFT JOIN count_registry AS pr ON (pr.product_id = p.id AND pr.cyclic_count_id = ct.cyclic_count_id AND pr.registry_type = 'physical')
        WHERE ct.cyclic_count_id = %s
        """
    # This work should be defered to a WORKER and use lazy dynamic to iterate through large list
    # First add m2m products then copy system registries from previous count WHERE DIFF != 0
    registries_pipeline = PandasAnalyzer(model=CountRegistry, session=db)
    registries_pipeline.export_excel_file(
        table_query=products_query, cyclic_count_id=cyclic_count_id)

    
def create_products_from_file(db:Session, cyclic_count_id: UUID, dataframe:DataFrame):
    sys_unit_tag= "U.Sistema"
    df = standarize_nulls_from_df(dataframe=dataframe)
    ccount = cyclic_count_crud.get_one_resource(
        session=db, resource_id=cyclic_count_id)
    result = test_models_creation(db=db, dataframe=dataframe)
    if result.status != 200:
        return result
    df[sys_unit_tag] = df[sys_unit_tag].fillna(0)
    def create_product_from_df(row):
        #product_category_crud
        category = locate_resource_from_name(db=db, model=ProductCategory, 
                                             res_crud=product_category_crud, name=row["Categoria"])
        munit= locate_resource_from_name(db=db, model=MeasureUnit, 
                                             res_crud=measure_unit_crud, name=row["U.Medida"])
        product = CreateProduct(
            name= row["Nombre"],
            code= row["Codigo"],
            sku= row["Sku"],
            unit_cost= row["CostoUnit."],
            measure_unit_id= munit.id,
            category_id=category.id,
            warehouse_ids=[],
            whlocation_ids=[],
            cyclic_count_ids=[ccount.id]   
        )
        
        created_prod = products_crud.create_resource(session=db, resource=product)
        count_registry = CreateCountRegistry(
            registry_type="system" ,
            registry_units=row[sys_unit_tag],
            registry_cost=row[sys_unit_tag] * created_prod.unit_cost,
            difference_cost=0,
            difference_units=0,
            product_id=created_prod.id,
            cyclic_count_id=ccount.id,
        )
        
        final_cr = count_registry_crud.create_resource(session=db, resource=count_registry)
        # count_registry_crud.c
        # print("GENERATED PRODUCT: ", created_prod)
    
    df.apply(create_product_from_df, axis=1)
    result = create_test_response(
        null_cat_idx=[], null_categories=[], nf_cat_idx=[], nf_cat_rows=[],
        null_mu_idx=[], null_mus=[], nf_mu_idx=[], nf_mu_rows=[])
    return result
    
