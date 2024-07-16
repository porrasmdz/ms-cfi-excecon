from typing import Optional
from pydantic import EmailStr
from uuid import UUID
from datetime import date 
from ..schemas import CreateSchema, ReadSchema, UpdateSchema


###COMPANY##########
class ReadCompany(ReadSchema):
    id: UUID
    name: str
    codename: Optional[str] = "CMY-AAA"
    phone_number: Optional[str]
    cellphone_number: Optional[str]
    email: EmailStr
    ruc: str
    foundation_date: Optional[date]

class CreateCompany(CreateSchema):
    name: str
    codename: Optional[str] 
    phone_number: Optional[str]
    cellphone_number: Optional[str]
    email: EmailStr
    ruc: str
    foundation_date: Optional[date]
    corporate_group_id: UUID

class UpdateCompany(UpdateSchema):
    name: Optional[str]
    codename: Optional[str] 
    phone_number: Optional[str]
    cellphone_number: Optional[str]
    email: Optional[EmailStr]
    ruc: Optional[str]
    foundation_date: Optional[date]
    corporate_group_id: Optional[UUID]

###CORPORATE GROUP
class ReadCorporateGroup(ReadSchema):
    id: UUID
    name: str
    description: Optional[str]
    

class CreateCorporateGroup(CreateSchema):
    name: str
    description: Optional[str]
    
class UpdateCorporateGroup(UpdateSchema):
    name: Optional[str]
    description: Optional[str]

###CONTACTS##############
class ReadContact(ReadSchema):
    id: UUID
    full_name : str
    contact_number : str
    alt_contact_number : Optional[str] 
    employee_charge : Optional[str] 
    email : EmailStr
    company_id : UUID 

class CreateContact(CreateSchema):
    full_name : str
    contact_number : str
    alt_contact_number : Optional[str] 
    employee_charge : Optional[str] 
    email : EmailStr
    company_id : UUID 
    
class UpdateContact(UpdateSchema):
    full_name : Optional[str]
    contact_number : Optional[str]
    alt_contact_number : Optional[str] 
    employee_charge : Optional[str] 
    email : Optional[EmailStr]
    company_id : Optional[UUID] 