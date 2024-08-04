from sqlalchemy import Boolean, Column, ForeignKey, Table
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List, Optional
from uuid import UUID, uuid4
from ..models import BaseSQLModel, Base, ccount_product_table, warehouse_ccount_table

warehouse_product_table = Table(
    "warehouse_product_table",
    Base.metadata,
    Column("warehouse_id", ForeignKey("warehouse.id"), primary_key=True),
    Column("product_id", ForeignKey("product.id"), primary_key=True)
)
whlocation_product_table = Table(
    "whlocation_product_table",
    Base.metadata,
    Column("warehouse_location_id", ForeignKey("warehouse_location.id"), primary_key=True),
    Column("product_id", ForeignKey("product.id"), primary_key=True)
)

class Warehouse(BaseSQLModel):
    __tablename__ = "warehouse"

    name : Mapped[Optional[str]] = mapped_column(default="Bodega AAA")
    country: Mapped[Optional[str]] = mapped_column(default="Ecuador")
    state: Mapped[Optional[str]] = mapped_column(default="Guayas")
    city: Mapped[Optional[str]] = mapped_column(default="Guayaquil")
    address: Mapped[Optional[str]] = mapped_column(default="Av AAA y Calle AAA, Edificio AAA")
    company_id :  Mapped[UUID] = mapped_column() #In this ms this does not exist its just an Id
    
    #Many to one
    warehouse_type_id : Mapped[UUID] = mapped_column(ForeignKey("warehouse_type.id"))
    warehouse_type : Mapped["WarehouseType"] = relationship(back_populates="warehouses") 

    #One to Many
    wh_locations : Mapped[Optional[List["WHLocation"]]] = relationship(back_populates="warehouse")

    #Many to Many
    products: Mapped[Optional[List["Product"]]] = relationship(
        secondary=warehouse_product_table, back_populates="warehouses"
    )
    cyclic_counts: Mapped[Optional[List["CyclicCount"]]] = relationship(
        secondary=warehouse_ccount_table, back_populates="warehouses"
    )

class WarehouseType(BaseSQLModel):
    __tablename__ = "warehouse_type"

    name : Mapped[str] = mapped_column()
    description : Mapped[Optional[str]] = mapped_column()

    warehouses : Mapped[Optional[List["Warehouse"]]] = relationship(back_populates="warehouse_type")
 

class WHLocation(BaseSQLModel):
    __tablename__ = "warehouse_location"

    id : Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name : Mapped[str] = mapped_column()
    description: Mapped[Optional[str]] = mapped_column()

    wh_location_type_id : Mapped[Optional[UUID]] = mapped_column(ForeignKey("warehouse_location_type.id"))
    wh_location_type: Mapped[Optional["WHLocation_Type"]] = relationship(back_populates="wh_locations")

    #recursive reference
    parent_id : Mapped[Optional[UUID]] = mapped_column(ForeignKey("warehouse_location.id"))#Parent Location
    parent_location : Mapped[Optional["WHLocation"]] = relationship(
                                                    back_populates="children_location", remote_side=[id]) #located_in
    children_location : Mapped[Optional[List["WHLocation"]]] = relationship(back_populates="parent_location") #are located within
    #warehouse ref
    warehouse_id : Mapped[UUID] = mapped_column(ForeignKey("warehouse.id"))
    warehouse : Mapped["Warehouse"] = relationship(back_populates="wh_locations")
    #products references
    products: Mapped[Optional[List["Product"]]] = relationship(
        secondary=whlocation_product_table, back_populates="warehouse_locations"
    )

class WHLocation_Type(BaseSQLModel):
    __tablename__ = "warehouse_location_type"
    name : Mapped[str] = mapped_column()
    wh_locations : Mapped[Optional[List["WHLocation"]]] = relationship(back_populates="wh_location_type")


class Product(BaseSQLModel):
    __tablename__ = "product"
    name : Mapped[str] = mapped_column()
    code : Mapped[Optional[str]] = mapped_column()
    sku : Mapped[Optional[str]] = mapped_column()
    unit_cost : Mapped[int] = mapped_column() #Multiplied by 100000
    
    #Many to one relation
    # cyclic_count_id : Mapped[UUID] = mapped_column() #Modify this

    measure_unit_id : Mapped[UUID] = mapped_column(ForeignKey("measure_unit.id"))
    measure_unit : Mapped["MeasureUnit"] = relationship(back_populates="products")
    
    category_id : Mapped[UUID] = mapped_column(ForeignKey("product_category.id"))
    category : Mapped["ProductCategory"] = relationship(back_populates="products")
    
    #Many2Many
    warehouses : Mapped[List["Warehouse"]] = relationship(
        secondary=warehouse_product_table, back_populates="products")
    warehouse_locations : Mapped[Optional[List["WHLocation"]]] = relationship(
        secondary=whlocation_product_table, back_populates="products")
    cyclic_counts : Mapped[List["CyclicCount"]] = relationship(
        secondary=ccount_product_table, back_populates="products"
    )
    #o2m
    count_registries : Mapped[Optional[List["CountRegistry"]]] = relationship(
        back_populates="product")
    
    
class ProductCategory(BaseSQLModel):
    __tablename__ = "product_category"
    id : Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name : Mapped[str] = mapped_column()
    short_codename: Mapped[str] = mapped_column()
    products : Mapped[Optional[List["Product"]]] = relationship(back_populates="category")
    #Make recursive reference here too
    #Recursive reference
    parent_id : Mapped[Optional[UUID]] = mapped_column(ForeignKey("product_category.id"))#Parent Location
    parent_category : Mapped[Optional["ProductCategory"]] = relationship(
                                                    back_populates="children_categories", remote_side=[id]) #located_in
    children_categories : Mapped[Optional[List["ProductCategory"]]] = relationship(back_populates="parent_category") #are located within
    ###

class MeasureUnit(BaseSQLModel):
    __tablename__ = "measure_unit"
    
    id : Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name : Mapped[str] = mapped_column()
    conversion_formula : Mapped[Optional[str]] = mapped_column()

    parent_id : Mapped[Optional[UUID]] = mapped_column(ForeignKey("measure_unit.id"))#Parent Measure Unit
    parent_mu : Mapped[Optional["MeasureUnit"]] =  relationship(back_populates="children_mu", remote_side=[id]) #located_in
    children_mu : Mapped[Optional[List["MeasureUnit"]]] =  relationship(back_populates="parent_mu") #are located within
    
    products : Mapped[Optional[List["Product"]]] = relationship(back_populates="measure_unit")
# class Report(Base):
#     __tablename__ = "inventory_report"
#     name : Mapped[str] = mapped_column()


from app.cyclic_count.models import CyclicCount, CountRegistry

metadata = Base.metadata
