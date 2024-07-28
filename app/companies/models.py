from sqlalchemy import Boolean, Column, ForeignKey, Table
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List, Optional
from uuid import UUID
from ..models import BaseSQLModel,Base
from datetime import date

class Company(BaseSQLModel):
    __tablename__ = "company"

    name : Mapped[str] = mapped_column(default="Compania AAA")
    codename : Mapped[Optional[str]] = mapped_column(default="CMY-AAA")
    phone_number : Mapped[Optional[str]] = mapped_column()
    cellphone_number : Mapped[Optional[str]] = mapped_column()
    email : Mapped[str] = mapped_column()
    ruc : Mapped[str] = mapped_column()
    foundation_date : Mapped[Optional[date]] = mapped_column()
    
    contacts : Mapped[Optional[List["Contact"]]] = relationship(back_populates="company")
    #Many to one
    corporate_group_id : Mapped[UUID] = mapped_column(ForeignKey("corporate_group.id"))
    corporate_group : Mapped["CorporativeGroup"] = relationship(back_populates="companies") 


class CorporativeGroup(BaseSQLModel):
    __tablename__ = "corporate_group"

    name : Mapped[str] = mapped_column()
    description : Mapped[Optional[str]] = mapped_column()

    companies : Mapped[Optional[List["Company"]]] = relationship(back_populates="corporate_group")
 
class Contact(BaseSQLModel):
    #TODO: Add Working Hours - Availability times
    __tablename__ = "contact"
    full_name : Mapped[str] = mapped_column()
    contact_number : Mapped[str] = mapped_column()
    alt_contact_number : Mapped[Optional[str]] = mapped_column()
    employee_charge : Mapped[str] = mapped_column()
    email : Mapped[str] = mapped_column()

    company_id : Mapped[UUID] = mapped_column(ForeignKey("company.id"))
    company : Mapped["Company"] = relationship(back_populates="contacts")
    
metadata = Base.metadata
