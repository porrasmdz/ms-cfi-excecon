from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from uuid import UUID
from app.utils import filters_to_sqlalchemy
from app.dependencies import get_table_query_body
from app.companies.models import Company, CorporativeGroup, Contact
from app.schemas import TableQueryBody, PaginatedResource
from . import service, schemas
from ..database import get_session

router = APIRouter()

# Company routes
@router.get("/companies/", response_model=PaginatedResource[schemas.DetailedCompany])
def read_companies(response: Response,
                   tqb: TableQueryBody = Depends(get_table_query_body), 
                   session: Session = Depends(get_session) ):
    filters = filters_to_sqlalchemy(model=Company, filters=tqb.filters) 
    (total_results, results)= service.get_companies(model=Company, filters=filters, 
                                                       tqb=tqb, session=session)
    
    response.headers['Access-Control-Expose-Headers'] = 'Content-Range'
    response.headers["Content-Range"] = f"companies {tqb.skip}-{tqb.limit}/{total_results}"
    response_resource = PaginatedResource(totalResults=total_results, results=results, 
                                 skip= tqb.skip, limit=tqb.limit)
    
    return response_resource

@router.get("/companies/{company_id}", response_model=schemas.DetailedCompany)
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
@router.get("/corporative_groups/", response_model=PaginatedResource[schemas.ReadCorporateGroup])
def read_corporative_groups(response: Response,
                            tqb: TableQueryBody = Depends(get_table_query_body), 
                            session: Session = Depends(get_session)):
    filters = filters_to_sqlalchemy(model=CorporativeGroup, filters=tqb.filters) 
    (total_results, results)= service.get_corporate_groups(model=CorporativeGroup, filters=filters, 
                                                       tqb=tqb, session=session)
    
    response.headers['Access-Control-Expose-Headers'] = 'Content-Range'
    response.headers["Content-Range"] = f"groups {tqb.skip}-{tqb.limit}/{total_results}"
    response_resource = PaginatedResource(totalResults=total_results, results=results, 
                                 skip= tqb.skip, limit=tqb.limit)
    return response_resource

@router.get("/corporative_groups/{corporative_group_id}", response_model=schemas.DetailedCorporateGroup)
def read_corporative_group(corporative_group_id: UUID, session: Session = Depends(get_session)):
    session_corporative_group = service.get_corporate_group(session, corporate_group_id=corporative_group_id)
    if session_corporative_group is None:
        raise HTTPException(status_code=404, detail="CorporativeGroup not found")
    return session_corporative_group

@router.post("/corporative_groups/", response_model=schemas.ReadCorporateGroup)
def create_corporative_group(corporative_group: schemas.CreateCorporateGroup, session: Session = Depends(get_session)):
    return service.create_corporate_group(session=session, corporate_group=corporative_group)

@router.put("/corporative_groups/{corporative_group_id}", response_model=schemas.ReadCorporateGroup)
def update_corporative_group(corporative_group_id: UUID, corporative_group: schemas.UpdateCorporateGroup, session: Session = Depends(get_session)):
    return service.update_corporate_group(session=session, corporate_group=corporative_group, corporate_group_id=corporative_group_id)

@router.delete("/corporative_groups/{corporative_group_id}", response_model=schemas.ReadCorporateGroup)
def delete_corporative_group(corporative_group_id: UUID, session: Session = Depends(get_session)):
    return service.delete_corporate_group(session=session, corporate_group_id=corporative_group_id)

# Contact routes
@router.get("/contacts/", response_model=PaginatedResource[schemas.ReadContact])
def read_contacts(response: Response,
                tqb: TableQueryBody = Depends(get_table_query_body),
                session: Session = Depends(get_session)):
    filters = filters_to_sqlalchemy(model=Contact, filters=tqb.filters) 
    (total_results, results)= service.get_contacts(model=Contact, filters=filters, 
                                                       tqb=tqb, session=session)
    
    response.headers['Access-Control-Expose-Headers'] = 'Content-Range'
    response.headers["Content-Range"] = f"contacts {tqb.skip}-{tqb.limit}/{total_results}"
    response = PaginatedResource(totalResults=total_results, results=results, 
                                 skip= tqb.skip, limit=tqb.limit)
    return response

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