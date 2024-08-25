from typing import Any, List, Optional
from uuid import UUID
from fastapi import HTTPException, status
from pandas import DataFrame
from pydantic import BaseModel
from sqlalchemy import Column, Table, func, select

from sqlalchemy.orm import Session
import pandas as pd
from app.cyclic_count.models import CyclicCount
from app.database import Base
from .service import cyclic_count_crud
general_client_info = Table(
    "general_client_info",
    Base.metadata,
    Column("ruc"),
    Column("codename"),
    Column("company"),
    Column("warehouse"),
    Column("country"),
    Column("state"),
    Column("city"),
    Column("address"),
    Column("cyclic_count_id")
)
wh_control_data = Table(
    "wh_control_data",
    Base.metadata,
    Column("cyclic_count_id"),
    Column("sys_registries"),
    Column("sys_unit"),
    Column("total_usd_system")
)
cyclic_count_history = Table(
    "cyclic_count_history",
    Base.metadata,
    Column("cyclic_count_id"),
    Column("warehouse"),
    Column("product_id"),
    Column("code"),
    Column("name"),
    Column("sku"),
    Column("unit_cost"),
    Column("measure_unit"),
    Column("category"),
    Column("system_units"),
    Column("physical_units"),
    Column("diff_units"),
    Column("total_usd_system"),
    Column("total_usd_physical"),
    Column("total_usd_diff"),
)


def get_report_by_ccount_id(session: Session, cyclic_count_id: UUID):
    gcit = session.execute(general_client_info.select().where(
        general_client_info.c.cyclic_count_id == cyclic_count_id)).first()
    wcdt = session.execute(wh_control_data.select().where(
        wh_control_data.c.cyclic_count_id == cyclic_count_id)).first()
    client_info = ClientInfo(company_name=gcit.company, company_province=gcit.state,
                             company_city=gcit.city, company_address=gcit.address)
    warehouse_control_data = WarehouseControlData(original_registries=wcdt.sys_registries,
                                                  original_units=str(
                                                      wcdt.sys_unit),
                                                  original_cost=str(wcdt.total_usd_system))
    warehouse_info = WarehouseInfo(warehouse_name=gcit.warehouse, warehouse_type="",
                                   warehouse_address=gcit.address, warehouse_supervisor="")
    responsibles = CountResponsibles(users=[])
    count_summary = get_count_summary(
        session=session, cyclic_count_id=cyclic_count_id)
    gcinfo = GeneralClientInfo(client_data=client_info, wh_data=warehouse_info,
                               count_responsibles=responsibles, wh_contrl_data=warehouse_control_data)
    return CyclicCountSummaryResults(general_client_info=gcinfo,
                                     count_summary=count_summary)

def get_count_summary(session: Session, cyclic_count_id: UUID):
    query = str(cyclic_count_history.select().where(
        cyclic_count_history.c.cyclic_count_id == cyclic_count_id))
    query = query.replace(":cyclic_count_id_1", "%s")
    df: DataFrame = pd.read_sql(query, session.bind, params=(cyclic_count_id,))
    numeric_columns = df.select_dtypes(include=['number']).columns
    df[numeric_columns] = df[numeric_columns].fillna(0)
    df = df.astype({'physical_units': 'int', 'diff_units': 'int', 'total_usd_system': 'int',
                    'total_usd_physical': 'int', 'total_usd_diff': 'int'})

    inv_univ = InventoryUniverse(system_registries=df['system_units'].count(),
                                 system_units=str(df['system_units'].sum()),
                                 system_t_cost=str(
                                     df['total_usd_system'].sum()),
                                 physical_registries=df['physical_units'].count(
    ),
        physical_units=str(
                                     df['physical_units'].sum()),
        physical_t_cost=str(df['total_usd_physical'].sum()))
    # PROB WILL HAVE TO IGNORE NOT COUNTED, NOT IGNORING BY NOW
    # VALIDATE TABLE OPERATION BY REWRITING DIFF COLS, DONT TRUST SOURCE
    no_diff_mask = (df['system_units'].round(
        1) - df['physical_units'].round(1) == 0)
    no_diff_df = df.loc[no_diff_mask]
    diff_df = df.loc[~no_diff_mask]

    obtained_results = ObtainedResults(no_diff_registries=no_diff_df['physical_units'].count(),
                                       no_diff_units=str(
                                           no_diff_df['physical_units'].sum()),
                                       no_diff_t_cost=str(
                                           no_diff_df['total_usd_physical'].sum()),
                                       diff_registries=diff_df['physical_units'].count(
    ),
        diff_units=str(
                                           diff_df['physical_units'].sum()),
        diff_t_cost=str(diff_df['total_usd_physical'].sum()))

    difference_serie = diff_df['system_units'] - diff_df['physical_units']
    total_usd_diff_serie = diff_df['total_usd_system'] - \
        diff_df['total_usd_physical']
    abs_val_diff_serie = difference_serie.abs()
    abs_val_total_usd_diff_serie = total_usd_diff_serie.abs()

    reference_data = ReferenceData(abs_diff_registries=abs_val_diff_serie.count(),
                                   abs_diff_units=str(
                                       abs_val_diff_serie.sum()),
                                   abs_diff_t_cost=str(
                                       abs_val_total_usd_diff_serie.sum()),
                                   net_diff_registries=difference_serie.count(),
                                   net_diff_units=str(difference_serie.sum()),
                                   net_diff_t_cost=str(total_usd_diff_serie.sum()))

    exceeding_serie = difference_serie[difference_serie[:] > 0]
    lacking_serie = difference_serie[difference_serie[:] < 0]
    total_usd_exceeding = total_usd_diff_serie[total_usd_diff_serie[:] > 0]
    total_usd_lacking = total_usd_diff_serie[total_usd_diff_serie[:] < 0]

    difference_details = DifferenceDetails(exceeding_registries=exceeding_serie.count(),
                                           exceeding_units=str(
                                               exceeding_serie.sum()),
                                           exceeding_t_cost=str(
                                               total_usd_exceeding.sum()),
                                           lacking_registries=lacking_serie.count(),
                                           lacking_units=str(
                                               lacking_serie.sum()),
                                           lacking_t_cost=str(total_usd_lacking.sum()))
    final_values = FinalValues(physical_t_cost=str(df['total_usd_physical'].sum()),
                               system_t_cost=str(df['total_usd_system'].sum()),
                               diff_t_cost=str(total_usd_diff_serie.sum()),
                               exceeding_t_cost=str(total_usd_exceeding.sum()),
                               lacking_t_cost=str(total_usd_lacking.sum()))
    count_summary = CountSummary(inv_universe=inv_univ,
                                 obtained_res=obtained_results,
                                 ref_data=reference_data,
                                 diff_details=difference_details,
                                 final_values=final_values)
    return count_summary

class CyclicCountSummaryResults(BaseModel):
    general_client_info: "GeneralClientInfo"
    count_summary: "CountSummary"


class ClientInfo(BaseModel):
    company_name: str
    company_province: str
    company_city: str
    company_address: str


class WarehouseInfo(BaseModel):
    warehouse_name: str
    warehouse_type: str
    warehouse_address: str
    warehouse_supervisor: str


class CountResponsibles(BaseModel):
    users: List[Any] = []

# THIS HAS TO BE ON FIRST CYCLIC_COUNT ONLY, CODE SHOULD BACKTRACK TO GET IT


class WarehouseControlData(BaseModel):
    original_registries: int
    original_units: str
    original_cost: str


class GeneralClientInfo(BaseModel):
    client_data: ClientInfo
    wh_data: WarehouseInfo
    count_responsibles: CountResponsibles
    wh_contrl_data: WarehouseControlData

####################################
# Informacion General del Cliente
####################################
# Datos del Cliente
# Company Name
# Company Province
# Company City
# Company Address

# Datos de Bodega
# Warehouse Name
# Warehouse Type
# Warehouse Address
# Warehouse Supervisor

# Responsables de Conteo
# Tabla Contact[Nombre, Correo, Telefono]

# Datos del sistema de bodega (CONTROL)
# Registros Originales Sistema X
# U. Sistema X
# Costo Total Sistema X

######################################
# Resumen del Conteo
######################################


class InventoryUniverse(BaseModel):
    system_registries: int
    system_units: str
    system_t_cost: str
    physical_registries: int
    physical_units: str
    physical_t_cost: str


class ObtainedResults(BaseModel):
    no_diff_registries: int
    no_diff_units: str
    no_diff_t_cost: str
    diff_registries: int
    diff_units: str
    diff_t_cost: str


class ReferenceData(BaseModel):
    abs_diff_registries: int
    abs_diff_units: str
    abs_diff_t_cost: str
    net_diff_registries: int
    net_diff_units: str
    net_diff_t_cost: str


class DifferenceDetails(BaseModel):
    exceeding_registries: int
    exceeding_units: str
    exceeding_t_cost: str
    lacking_registries: int
    lacking_units: str
    lacking_t_cost: str


class FinalValues(BaseModel):
    physical_t_cost: str
    system_t_cost: str
    diff_t_cost: str
    exceeding_t_cost: str
    lacking_t_cost: str


class CountSummary(BaseModel):
    inv_universe: InventoryUniverse
    obtained_res: ObtainedResults
    ref_data: ReferenceData
    diff_details: DifferenceDetails
    final_values: FinalValues
# Universo del Inventario
# Registros en Sistema
# Unidades en Sistema
# Total USD Sistema
# Registros en Fisico
# Unidades en Bodega
# Total USD Fisico

# Resultados Obtenidos
# Registros sin Diferencia
# U sin Diferencia
# Total USD sin Diferencia
# [Los de abajo -> Registros en Sistema - Registros sin Diferencia y asi con los sgts.]
# Registros con Diferencia
# U.Sistema con Diferencia (Por Conciliar)
# Total USD con Diferencia (Por Conciliar)

# Datos Referenciales
# Unidades con diff absoluta [Sistema - diff total] (diff total = sobrantes-faltantes)
# Total USD con diff absoluta [Sistema - diff total] (diff total = sobrantes-faltantes)
# Unidades con diff neta [Sistema - diff neta] (diff neta = sobrantes+faltantes)

# Detalle de Diferencias
# Registros sobrantes
# Unidades sobrantes
# Total USD Sobrantes
# Registros faltantes
# Unidades Faltantes
# Total USD Faltantes

# Valores Finales
# Total USD Fisico
# Total USD Sistema
# Diff final en USD
# Total USD Sobrantes
# Total USD Faltantes

#########################################
# RESUMEN - CyclicCountHistory
#########################################
# class CyclicCountHistory(BaseModel):
#     column_headers: List[str]
#     data: DataFrame

# Productos sin Diferencia (Registros [Filas] totales X | Total USD $** | Neto USD $**)
# [Codigo | Product Name | Full Location Code?? | Warehouse | WHLocation Name |
#    Costo Unit | U.Sistema | U.Fisico | Unid. Medida | U.Diferencia | Total USD. Sistema |
#    Total USD. Fisico | Total USD Diferencia | Comentario Adicional]
# Productos con Diferencia (Registros [Filas] totales X | Total USD $** | Neto USD $**)
# [Codigo | Product Name | Full Location Code?? | Warehouse | WHLocation Name |
#    Costo Unit | U.Sistema | U.Fisico | Unid. Medida | U.Diferencia | Total USD. Sistema |
#    Total USD. Fisico | Total USD Diferencia | Comentario Adicional]

# Productos Sobrantes (Registros [Filas] totales X | Total USD $**)
# [Codigo | Product Name | Full Location Code?? | Warehouse | WHLocation Name |
#    Costo Unit | U.Sistema | U.Fisico | Unid. Medida | U.Diferencia | Total USD. Sistema |
#    Total USD. Fisico | Total USD Diferencia | Comentario Adicional]

# Productos Faltantes (Registros [Filas] totales X | Total USD $**)
# [Codigo | Product Name | Full Location Code?? | Warehouse | WHLocation Name |
#    Costo Unit | U.Sistema | U.Fisico | Unid. Medida | U.Diferencia | Total USD. Sistema |
#    Total USD. Fisico | Total USD Diferencia | Comentario Adicional]


#########################################
# Conteos Previos  - PreviousCyclicCounts
#########################################
def map_df_to_schema(df: DataFrame) -> List[dict]:
    result = []
    def get_column_val_if_exists(row, tag):
        return str(row[tag]) if tag in row and pd.notna(row[tag]) else None
    for _, row in df.iterrows():
        history_row = CCountHistoryRow(
            code=row['code'],
            product_name=row['name'],
            location_code="n/f",#row['location_code'],
            warehouse=row['warehouse'],
            warehouse_location="n/f",#row['warehouse_location'],
            unit_cost=str(row['unit_cost']),
            system_units=str(row['system_units']),
            physical_units_one=get_column_val_if_exists(row, "1_physical_units"),
            physical_units_two=get_column_val_if_exists(row, "2_physical_units"),
            physical_units_three=get_column_val_if_exists(row, "3_physical_units"),
            physical_units_four=get_column_val_if_exists(row, "4_physical_units"),
            physical_units_five=get_column_val_if_exists(row, "5_physical_units"),  
            physical_units_six=get_column_val_if_exists(row, "6_physical_units"),
            physical_units_seven=get_column_val_if_exists(row, "7_physical_units"),
            adjustment=str(row['adjustment']) if 'adjustment' in row else "n/a",
            final_physical_units=str(row['final_physical_units']),
            measure_units=row['measure_unit'],
            difference_units=str(row['diff_units']),
            total_usd_system=str(row['total_usd_system']),
            total_usd_physical=str(row['total_usd_physical']),
            total_usd_difference=str(row['total_usd_diff']),
            commentary=row.get('commentary', None)  # Si existe la columna 'commentary'
        )

        result.append(history_row.model_dump())
    return result

def get_ccount_history(session: Session, cyclic_count_id: UUID, skip: int, limit: int):
    #TODO: MAP PENDING COLUMNS 
    ccount : CyclicCount =  cyclic_count_crud.get_one_resource(session=session,resource_id=cyclic_count_id)
    
    #Determine amnt of prev ccounts
    def iterate_ccounts(itlist: list, ccount: CyclicCount):
        if len(itlist) > 7:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="CyclicCount has more than seven previous counts")
        if ccount.previous_ccount is not None:
            itlist.append(ccount)
            return iterate_ccounts(itlist, ccount.previous_ccount)
        else:
            itlist.append(ccount)
            return itlist
    prev_ccounts = [ccount]
    if ccount.previous_ccount is not None:
        prev_ccounts = []
        prev_ccounts = iterate_ccounts(prev_ccounts, ccount)
    #PER EACH CCOUNT EXTRACT THE PHYSICAL COUNT COLUMN AND APPEND IT TO TABLE, OTHER COLUMNS APPEND 0 AND RETURM CCOUNTHISTORYROWS
    llen = len(prev_ccounts)
    first_count = prev_ccounts[llen - 1]
    base_query = select(cyclic_count_history).where(cyclic_count_history.c.cyclic_count_id == first_count.id)
    query = str(base_query.limit(limit).offset(skip))
    query = query.replace(":cyclic_count_id_1", "%s")
    query = query.replace(":param_1", "%s")
    query = query.replace(":param_2", "%s")
    main_df = pd.read_sql(str(query), session.bind, params=(first_count.id, limit, skip)).loc[::,"warehouse":"total_usd_diff"]
    result_colums_tags = []
    for count_idx in range(llen):
        count_num = llen - count_idx
        curr_row_name = f'{count_num}_physical_units'
        result_colums_tags.append(curr_row_name)
        curr_ccount = prev_ccounts[count_idx]
        query = str(select(cyclic_count_history).where(cyclic_count_history.c.cyclic_count_id == curr_ccount.id).limit(limit).offset(skip))
        query = query.replace(":cyclic_count_id_1", "%s")
        query = query.replace(":param_1", "%s")
        query = query.replace(":param_2", "%s")
        
        df = pd.read_sql(str(query), session.bind, params=(curr_ccount.id, limit, skip))[["product_id", "physical_units"]] 
        df.rename(columns={'physical_units': curr_row_name}, inplace=True) 
        main_df = main_df.merge(df, how="left", on="product_id")
    main_df['final_physical_units'] = main_df[result_colums_tags].bfill(axis=1).iloc[:, 0]
    main_df['final_physical_units'] = main_df['final_physical_units'].fillna(0)
    results = map_df_to_schema(main_df)
    count_query = select(func.count()).select_from(cyclic_count_history).where(cyclic_count_history.c.cyclic_count_id == first_count.id)
    total_results = session.execute(count_query).scalar()
    return (total_results,results)

class CCountHistoryRow(BaseModel):
    code: str
    product_name: str
    location_code: str
    warehouse: str
    warehouse_location: str
    unit_cost: str
    system_units: str
    physical_units_one: Optional[str] = None
    physical_units_two: Optional[str] = None
    physical_units_three: Optional[str] = None
    physical_units_four: Optional[str] = None
    physical_units_five: Optional[str] = None
    physical_units_six: Optional[str] = None
    physical_units_seven: Optional[str] = None
    adjustment: str
    final_physical_units: str
    measure_units: str
    difference_units: str
    total_usd_system: str
    total_usd_physical: str
    total_usd_difference: str
    commentary: Optional[str] = None

# [Codigo | Product Name | Full Location Code?? | Warehouse | WHLocation Name |
#    Costo Unit | U.Sistema | U. 1C | U. 2C | U.3C | Ajuste | U. Fisico Final | Unid. Medida | U.Diferencia | Total USD. Sistema |
#    Total USD. Fisico | Total USD Diferencia | Comentario Adicional]
