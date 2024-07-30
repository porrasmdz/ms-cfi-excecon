from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Table, Column, ForeignKey
from typing import Optional
from datetime import datetime
from .database import Base, engine
from uuid import UUID, uuid4

engine = engine

ccount_product_table = Table(
    "ccount_product_table",
    Base.metadata,
    Column("cyclic_count_id", ForeignKey("cyclic_count.id"), primary_key=True),
    Column("product_id", ForeignKey("product.id"), primary_key=True)
)
warehouse_ccount_table = Table(
    "warehouse_ccount_table",
    Base.metadata,
    Column("warehouse_id", ForeignKey("warehouse.id"), primary_key=True),
    Column("cyclic_count_id", ForeignKey("cyclic_count.id"), primary_key=True)
)

class BaseSQLModel(Base):
    __abstract__ = True
    id : Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    is_archived : Mapped[bool] = mapped_column(default=False)
    created_at : Mapped[datetime] = mapped_column()
    updated_at : Mapped[datetime] = mapped_column()
    deleted_at : Mapped[Optional[datetime]] = mapped_column()
