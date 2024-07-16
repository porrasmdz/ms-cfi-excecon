from sqlalchemy import Boolean, Column, ForeignKey, Table
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List, Optional, Literal
from uuid import UUID, uuid4
from ..models import BaseSQLModel, ccount_product_table
from datetime import datetime
from app.inventory.models import Product

class CyclicCount(BaseSQLModel):
    __tablename__ = "cyclic_count"
    id : Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name : Mapped[str] = mapped_column()
    status : Mapped[Optional[str]] = mapped_column() #Abierto, Revision, Cerrado
    count_type : Mapped[str] = mapped_column(default="Primer Conteo") #Primero, Segundo, Tercero, Cuarto, Conciliacion ...
    count_date_start : Mapped[datetime] = mapped_column(default_factory=datetime.now) 
    count_date_finish : Mapped[datetime] = mapped_column(default_factory=datetime.now)

    products : Mapped["Product"] = relationship(
        secondary=ccount_product_table, back_populates="cyclic_counts"
    )
    count_registries : Mapped[Optional[List["CountRegistry"]]] = relationship(back_populates="cyclic_count")
    
    #Recursive reference
    parent_id : Mapped[Optional[UUID]] = mapped_column(ForeignKey("cyclic_count.id"))#Parent Location
    previous_ccount : Mapped[Optional["CyclicCount"]] = relationship(
                                                    back_populates="next_ccount", remote_side=[id]) #located_in
    next_ccount : Mapped[Optional["CyclicCount"]] = relationship(back_populates="previous_ccount") #are located within
    ###
   

RegistryType = Literal["system", "physical", "consolidated"]

#Multiplied by 100000
class CountRegistry(BaseSQLModel):
    __tablename__ = "count_registry"
    registry_type : Mapped[RegistryType] #system, physical, consolidated 
    registry_units : Mapped[int] = mapped_column()
    registry_cost : Mapped[int] = mapped_column()
    difference_units : Mapped[int] = mapped_column()
    difference_cost : Mapped[int] = mapped_column()

    product_id : Mapped[UUID] = mapped_column(ForeignKey("product.id"))
    product : Mapped["Product"] = relationship(back_populates="count_registries")

    cyclic_count_id : Mapped[UUID] = mapped_column(ForeignKey("cyclic_count.id"))
    cyclic_count : Mapped["CyclicCount"] = relationship(back_populates="count_registries")
    
    activity_registries : Mapped[List["ActivityRegistry"]] = relationship(back_populates="count_registry")

class ActivityRegistry(BaseSQLModel):
    __tablename__ = "activity_registry"
    detail : Mapped[str] = mapped_column()
    commentary : Mapped[str] = mapped_column()
    user : Mapped[UUID] = mapped_column()
    
    count_registry_id : Mapped[UUID] = mapped_column(ForeignKey("count_registry.id"))
    count_registry : Mapped["CountRegistry"] = relationship(back_populates="activity_registries")