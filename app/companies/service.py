from sqlalchemy.orm import Session
from fastapi import HTTPException
from uuid import UUID

from .models import (
    Company, CorporativeGroup, Contact )



def update_validating_deletion_time(object, key, value):
    if value is not None and key != "deleted_at":
        setattr(object, key, value)
    if key == "deleted_at":
        setattr(object, key, value)

def get_companies(session: Session, skip: int = 0, limit: int = 100):
    return session.query(Company).offset(skip).limit(limit).all()

def get_company(session: Session, company_id: UUID):
    return session.query(Company).filter(Company.id == company_id).first()

def create_company(session: Session, company: Company):
    session_company = Company(**company.dict())
    session.add(session_company)
    session.commit()
    session.refresh(session_company)
    return session_company

def update_company(session: Session, company_id: UUID, company: Company):
    session_company = session.query(Company).filter(Company.id == company_id).first()
    if session_company:
        for key, value in company.dict(exclude_unset=True).items():
            update_validating_deletion_time(session_company, key, value)
            
        session.commit()
        session.refresh(session_company)
    else:
        raise HTTPException(status_code=404, detail=f"Company with id {company_id} not found")
    return session_company

def delete_company(session: Session, company_id: UUID):
    session_company = session.query(Company).filter(Company.id == company_id).first()
    if session_company:
        session.delete(session_company)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f"Company with id {company_id} not found")
    return session_company

# CRUD Operations for CorporativeGroup

def get_corporate_groups(session: Session, skip: int = 0, limit: int = 100):
    return session.query(CorporativeGroup).offset(skip).limit(limit).all()

def get_corporate_group(session: Session, corporate_group_id: UUID):
    return session.query(CorporativeGroup).filter(CorporativeGroup.id == corporate_group_id).first()

def create_corporate_group(session: Session, corporate_group: CorporativeGroup):
    session_corporate_group = CorporativeGroup(**corporate_group.dict())
    session.add(session_corporate_group)
    session.commit()
    session.refresh(session_corporate_group)
    return session_corporate_group

def update_corporate_group(session: Session, corporate_group_id: UUID, corporate_group: CorporativeGroup):
    session_corporate_group = session.query(CorporativeGroup).filter(CorporativeGroup.id == corporate_group_id).first()
    if session_corporate_group:
        for key, value in corporate_group.dict(exclude_unset=True).items():
            update_validating_deletion_time(session_corporate_group, key, value)
        session.commit()
        session.refresh(session_corporate_group)
    else:
        raise HTTPException(status_code=404, detail=f"CorporativeGroup with id {corporate_group_id} not found")
    return session_corporate_group

def delete_corporate_group(session: Session, corporate_group_id: UUID):
    session_corporate_group = session.query(CorporativeGroup).filter(CorporativeGroup.id == corporate_group_id).first()
    if session_corporate_group:
        session.delete(session_corporate_group)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f"CorporativeGroup with id {corporate_group_id} not found")
    return session_corporate_group

# CRUD Operations for Contact

def get_contacts(session: Session, skip: int = 0, limit: int = 100):
    return session.query(Contact).offset(skip).limit(limit).all()

def get_contact(session: Session, contact_id: UUID):
    return session.query(Contact).filter(Contact.id == contact_id).first()

def create_contact(session: Session, contact: Contact):
    session_contact = Contact(**contact.dict())
    session.add(session_contact)
    session.commit()
    session.refresh(session_contact)
    return session_contact

def update_contact(session: Session, contact_id: UUID, contact: Contact):
    session_contact = session.query(Contact).filter(Contact.id == contact_id).first()
    if session_contact:
        for key, value in contact.dict(exclude_unset=True).items():
            update_validating_deletion_time(session_contact, key, value)
        session.commit()
        session.refresh(session_contact)
    else:
        raise HTTPException(status_code=404, detail=f"Contact with id {contact_id} not found")
    return session_contact

def delete_contact(session: Session, contact_id: UUID):
    session_contact = session.query(Contact).filter(Contact.id == contact_id).first()
    if session_contact:
        session.delete(session_contact)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f"Contact with id {contact_id} not found")
    return session_contact