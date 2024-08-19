from typing import List
from pandas import DataFrame
from pydantic import BaseModel

from app.auth.models import User

def ClientInfo(BaseModel):
    company_name: str
    company_province: str
    company_city: str
    company_address: str

def WarehouseInfo(BaseModel):
    warehouse_name: str
    warehouse_type: str
    warehouse_address: str
    warehouse_supervisor: str

def CountResponsibles(BaseModel):
    users: List[User] = []

def WarehouseControlData(BaseModel):
    original_registries: int
    original_units: str
    original_cost: str

def GeneralClientInfo(BaseModel):
    client_data: ClientInfo
    wh_data: WarehouseInfo
    count_responsibles: CountResponsibles
    wh_contrl_data: WarehouseControlData

####################################
###Informacion General del Cliente
####################################
####Datos del Cliente
#Company Name
#Company Province
#Company City
#Company Address

####Datos de Bodega
#Warehouse Name
#Warehouse Type
#Warehouse Address
#Warehouse Supervisor

####Responsables de Conteo
#Tabla Contact[Nombre, Correo, Telefono]

####Datos del sistema de bodega (CONTROL)
#Registros Originales Sistema X
#U. Sistema X
#Costo Total Sistema X

######################################
#####Resumen del Conteo
######################################

def InventoryUniverse(BaseModel):
    system_registries: int
    system_units: str
    system_t_cost: str
    physical_registries: int
    physical_units: str
    physical_t_cost: str
def ObtainedResults(BaseModel):
    no_diff_registries: int
    no_diff_units: str
    no_diff_t_cost: str
    diff_registries: int
    diff_units: str
    diff_t_cost: str
def ReferenceData(BaseModel):
    abs_diff_registries: int
    abs_diff_units: str
    abs_diff_t_cost: str
    net_diff_registries: int
    net_diff_units: str
    net_diff_t_cost: str
def DifferenceDetails(BaseModel):
    exceeding_registries: int
    exceeding_units: str
    exceeding_t_cost: str
    lacking_registries: int
    lacking_units: str
    lacking_t_cost: str

def FinalValues(BaseModel):
    physical_t_cost: str
    system_t_cost: str
    diff_t_cost: str
    exceeding_t_cost: str
    lacking_t_cost: str

def CountSummary(BaseModel):
    inv_universe: InventoryUniverse
    obtained_res: ObtainedResults
    ref_data: ReferenceData
    diff_details: DifferenceDetails
    final_values: FinalValues
####Universo del Inventario
#Registros en Sistema
#Unidades en Sistema
#Total USD Sistema
#Registros en Fisico
#Unidades en Bodega
#Total USD Fisico

####Resultados Obtenidos
#Registros sin Diferencia
#U sin Diferencia
#Total USD sin Diferencia
#[Los de abajo -> Registros en Sistema - Registros sin Diferencia y asi con los sgts.]
#Registros con Diferencia
#U.Sistema con Diferencia (Por Conciliar)
#Total USD con Diferencia (Por Conciliar)

####Datos Referenciales
#Unidades con diff absoluta [Sistema - diff total] (diff total = sobrantes-faltantes)
#Total USD con diff absoluta [Sistema - diff total] (diff total = sobrantes-faltantes)
#Unidades con diff neta [Sistema - diff neta] (diff neta = sobrantes+faltantes)

####Detalle de Diferencias
#Registros sobrantes
#Unidades sobrantes
#Total USD Sobrantes
#Registros faltantes
#Unidades Faltantes
#Total USD Faltantes

####Valores Finales
#Total USD Fisico
#Total USD Sistema
#Diff final en USD 
#Total USD Sobrantes
#Total USD Faltantes

#########################################
###RESUMEN - SingleCyclicCount
#########################################
def CyclicCountHistory(BaseModel):
    column_headers: List[str]
    data: DataFrame

###Productos sin Diferencia (Registros [Filas] totales X | Total USD $** | Neto USD $**)
#[Codigo | Product Name | Full Location Code?? | Warehouse | WHLocation Name | 
#    Costo Unit | U.Sistema | U.Fisico | Unid. Medida | U.Diferencia | Total USD. Sistema |
#    Total USD. Fisico | Total USD Diferencia | Comentario Adicional]
###Productos con Diferencia (Registros [Filas] totales X | Total USD $** | Neto USD $**)
#[Codigo | Product Name | Full Location Code?? | Warehouse | WHLocation Name | 
#    Costo Unit | U.Sistema | U.Fisico | Unid. Medida | U.Diferencia | Total USD. Sistema |
#    Total USD. Fisico | Total USD Diferencia | Comentario Adicional]

##Productos Sobrantes (Registros [Filas] totales X | Total USD $**)
#[Codigo | Product Name | Full Location Code?? | Warehouse | WHLocation Name | 
#    Costo Unit | U.Sistema | U.Fisico | Unid. Medida | U.Diferencia | Total USD. Sistema |
#    Total USD. Fisico | Total USD Diferencia | Comentario Adicional]

##Productos Faltantes (Registros [Filas] totales X | Total USD $**)
#[Codigo | Product Name | Full Location Code?? | Warehouse | WHLocation Name | 
#    Costo Unit | U.Sistema | U.Fisico | Unid. Medida | U.Diferencia | Total USD. Sistema |
#    Total USD. Fisico | Total USD Diferencia | Comentario Adicional]


#########################################
###Conteos Previos  - PreviousCyclicCounts
#########################################
#[Codigo | Product Name | Full Location Code?? | Warehouse | WHLocation Name | 
#    Costo Unit | U.Sistema | U. 1C | U. 2C | U.3C | Ajuste | U. Fisico Final | Unid. Medida | U.Diferencia | Total USD. Sistema |
#    Total USD. Fisico | Total USD Diferencia | Comentario Adicional]

