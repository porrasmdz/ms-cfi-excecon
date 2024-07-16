from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from . import service, schemas
from ..database import get_session

router = APIRouter()

# Company routes
@router.get("/companies/", response_model=List[schemas.ReadCompany])
def read_companies(skip: int = 0, limit: int = 10, session: Session = Depends(get_session)):
    companies = service.get_companies(session, skip=skip, limit=limit)
    return companies

@router.get("/companies/{company_id}", response_model=schemas.ReadCompany)
def read_company(company_id: UUID, session: Session = Depends(get_session)):
    session_company = service.get_company(session, company_id=company_id)
    if session_company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return session_company

@router.post("/companies/", response_model=schemas.ReadCompany)
def create_company(company: schemas.CreateCompany, session: Session = Depends(get_session)):
    return service.create_company(session=session, company=company)

@router.put("/companies/{company_id}", response_model=schemas.ReadCompany)
def update_company(company_id: UUID, company: schemas.UpdateCompany, session: Session = Depends(get_session)):
    return service.update_company(session=session, company_id=company_id, company=company)

@router.delete("/companies/{company_id}", response_model=schemas.ReadCompany)
def delete_company(company_id: UUID, session: Session = Depends(get_session)):
    return service.delete_company(session=session, company_id=company_id)

# CorporativeGroup routes
@router.get("/corporative_groups/", response_model=List[schemas.ReadCorporativeGroup])
def read_corporative_groups(skip: int = 0, limit: int = 10, session: Session = Depends(get_session)):
    corporative_groups = service.get_corporative_groups(session, skip=skip, limit=limit)
    return corporative_groups

@router.get("/corporative_groups/{corporative_group_id}", response_model=schemas.ReadCorporativeGroup)
def read_corporative_group(corporative_group_id: UUID, session: Session = Depends(get_session)):
    session_corporative_group = service.get_corporative_group(session, corporative_group_id=corporative_group_id)
    if session_corporative_group is None:
        raise HTTPException(status_code=404, detail="CorporativeGroup not found")
    return session_corporative_group

@router.post("/corporative_groups/", response_model=schemas.ReadCorporativeGroup)
def create_corporative_group(corporative_group: schemas.CreateCorporativeGroup, session: Session = Depends(get_session)):
    return service.create_corporative_group(session=session, corporative_group=corporative_group)

@router.put("/corporative_groups/{corporative_group_id}", response_model=schemas.ReadCorporativeGroup)
def update_corporative_group(corporative_group_id: UUID, corporative_group: schemas.UpdateCorporativeGroup, session: Session = Depends(get_session)):
    return service.update_corporative_group(session=session, corporative_group_id=corporative_group_id, corporative_group=corporative_group)

@router.delete("/corporative_groups/{corporative_group_id}", response_model=schemas.ReadCorporativeGroup)
def delete_corporative_group(corporative_group_id: UUID, session: Session = Depends(get_session)):
    return service.delete_corporative_group(session=session, corporative_group_id=corporative_group_id)

# Contact routes
@router.get("/contacts/", response_model=List[schemas.ReadContact])
def read_contacts(skip: int = 0, limit: int = 10, session: Session = Depends(get_session)):
    contacts = service.get_contacts(session, skip=skip, limit=limit)
    return contacts

@router.get("/contacts/{contact_id}", response_model=schemas.ReadContact)
def read_contact(contact_id: UUID, session: Session = Depends(get_session)):
    session_contact = service.get_contact(session, contact_id=contact_id)
    if session_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return session_contact

@router.post("/contacts/", response_model=schemas.ReadContact)
def create_contact(contact: schemas.CreateContact, session: Session = Depends(get_session)):
    return service.create_contact(session=session, contact=contact)

@router.put("/contacts/{contact_id}", response_model=schemas.ReadContact)
def update_contact(contact_id: UUID, contact: schemas.UpdateContact, session: Session = Depends(get_session)):
    return service.update_contact(session=session, contact_id=contact_id, contact=contact)

@router.delete("/contacts/{contact_id}", response_model=schemas.ReadContact)
def delete_contact(contact_id: UUID, session: Session = Depends(get_session)):
    return service.delete_contact(session=session, contact_id=contact_id)