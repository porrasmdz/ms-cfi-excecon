from pydantic import BaseModel

def SingleCyclicCount(BaseModel):
    pass

def PreviousCyclicCounts(BaseModel):
    pass
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

