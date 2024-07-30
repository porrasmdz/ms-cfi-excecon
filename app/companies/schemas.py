from typing import Optional, List
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

class DetailedCompany(ReadSchema):
    id: UUID
    name: str
    codename: Optional[str] = "CMY-AAA"
    phone_number: Optional[str]
    cellphone_number: Optional[str]
    email: EmailStr
    ruc: str
    foundation_date: Optional[date]
    contacts: Optional[List["ReadContact"]]
    corporate_group: "ReadCorporateGroup"
    corporate_group_id: UUID

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
    name: Optional[str] = None
    codename: Optional[str] = None 
    phone_number: Optional[str] = None
    cellphone_number: Optional[str] = None
    email: Optional[EmailStr] = None
    ruc: Optional[str] = None
    foundation_date: Optional[date] = None
    corporate_group_id: Optional[UUID] = None

###CORPORATE GROUP
class ReadCorporateGroup(ReadSchema):
    id: UUID
    name: str
    description: Optional[str]

class DetailedCorporateGroup(ReadSchema):
    id: UUID
    name: str
    description: Optional[str]
    companies: Optional[List[ReadCompany]]

class CreateCorporateGroup(CreateSchema):
    name: str
    description: Optional[str]
    
class UpdateCorporateGroup(UpdateSchema):
    name: Optional[str] = None
    description: Optional[str] = None

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
    full_name : Optional[str] = None
    contact_number : Optional[str] = None
    alt_contact_number : Optional[str] = None 
    employee_charge : Optional[str] = None 
    email : Optional[EmailStr] = None
    company_id : Optional[UUID] = None