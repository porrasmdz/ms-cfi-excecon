import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi.testclient import TestClient
from app.main import app
from uuid import uuid4
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import  settings
from app.database import Base, get_session
from app.inventory.models import Product, MeasureUnit, ProductCategory, Warehouse, WarehouseType, WHLocation_Type, WHLocation
from app.cyclic_count.models import CyclicCount, CountRegistry, ActivityRegistry
from app.companies.models import Company, CorporativeGroup, Contact
from datetime import datetime

SQLALCHEMY_DATABASE_URL = settings.TEST_DB_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)


TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def sample_companies_data(db: Session):
    # Crear datos necesarios para las pruebas
    corp_group = CorporativeGroup(name="Group AAA", description="description",
                               created_at=datetime.now(), updated_at=datetime.now())
    company = Company(name="Unit 1", email="comp2@organization.com", 
                      ruc="0999999999001", corporate_group=corp_group,
                               created_at=datetime.now(), updated_at=datetime.now())
    contact = Contact(full_name="User Test", contact_number="0999999999", employee_charge="Employee",
                       email="user@organization.com", company=company,
                        created_at=datetime.now(), updated_at=datetime.now())
    db.add(corp_group)
    db.add(company)
    db.add(contact)
    db.commit()
    return {
        "company_id" : company.id,
        "corp_group_id" : corp_group.id,
        "contact_id" : contact.id,
    }

@pytest.fixture(scope="module")
def sample_product_category_mu_data(db: Session):
    # Crear datos necesarios para las pruebas
    category = ProductCategory(name="Category 1", short_codename="CAT1",
                               created_at=datetime.now(), updated_at=datetime.now())
    measure_unit = MeasureUnit(name="Unit 1",
                               created_at=datetime.now(), updated_at=datetime.now())
    db.add(category)
    db.add(measure_unit)
    db.commit()
    return {
        "category_id" : category.id,
        "measure_unit_id" : measure_unit.id,
    }

@pytest.fixture(scope="module")
def sample_product_data(db: Session):
    # Crear datos necesarios para las pruebas
    category = ProductCategory(name="Category 1", short_codename="CAT1",
                               created_at=datetime.now(), updated_at=datetime.now())
    measure_unit = MeasureUnit(name="Unit 1",
                               created_at=datetime.now(), updated_at=datetime.now())
   
    product = Product(name="My Product", unit_cost=100, 
                      category=category, measure_unit=measure_unit,
                      created_at=datetime.now(), updated_at=datetime.now())
    db.add(category)
    db.add(measure_unit)
    db.add(product)
    db.commit()
    return {
        "category_id" : category.id,
        "measure_unit_id" : measure_unit.id,
        "product_id" : product.id
    }

@pytest.fixture(scope="module")
def sample_data_warehouse(db: Session):
    # Crear datos de prueba
    warehouse_type_id = uuid4()
    warehouse_id = uuid4()
    wh_location_type_id = uuid4()
    wh_location_id = uuid4()

    warehouse_type = WarehouseType(id=warehouse_type_id, name="Type A", 
                                   description="Type A Description",
                                   created_at=datetime.now(), updated_at=datetime.now())
    alt_warehouse_type = WarehouseType(name="Type A", 
                                   description="Type A Description",
                                   created_at=datetime.now(), updated_at=datetime.now())
    warehouse = Warehouse(
        id=warehouse_id,
        name="Main Warehouse",
        country="Ecuador",
        state="Guayas",
        city="Guayaquil",
        address="Av AAA y Calle AAA, Edificio AAA",
        company_id=uuid4(),
        warehouse_type=warehouse_type,
        created_at=datetime.now(), 
        updated_at=datetime.now()
    )
    alt_warehouse = Warehouse(
        name="Main Warehouse",
        country="Ecuador",
        state="Guayas",
        city="Guayaquil",
        address="Av AAA y Calle AAA, Edificio AAA",
        company_id=uuid4(),
        warehouse_type=alt_warehouse_type,
        created_at=datetime.now(), 
        updated_at=datetime.now()
    )
    
    db.add(warehouse_type)
    db.add(warehouse)
    db.add(alt_warehouse_type)
    db.add(alt_warehouse)
    db.commit()

    wh_location_type = WHLocation_Type(id=wh_location_type_id, name="Shelf",
                                       created_at=datetime.now(), updated_at=datetime.now())
    wh_location = WHLocation(
        id=wh_location_id,
        name="Shelf 1",
        description="First shelf",
        wh_location_type=wh_location_type,
        warehouse=alt_warehouse,
        created_at=datetime.now(), 
        updated_at=datetime.now()
    )
    
    db.add(wh_location_type)
    db.add(wh_location)
    db.commit()

    return {
        "warehouse_id": warehouse_id,
        "warehouse_type_id": warehouse_type_id,
        "alt_warehouse_id": alt_warehouse.id,
        "alt_warehouse_type_id": alt_warehouse_type.id,
        "wh_location_id": wh_location_id,
        "wh_location_type_id": wh_location_type_id
    }
@pytest.fixture(scope="module")
def sample_data(db: Session):
    # Crear datos de prueba
    measure_unit = MeasureUnit( name="Unidad(es)", created_at=datetime.now(), 
                               updated_at=datetime.now())
    category = ProductCategory( name="Categoria Default", short_codename="CD", 
                               created_at=datetime.now(), updated_at=datetime.now())
    cyclic_count = CyclicCount( name="Test Count", count_type="Primer Conteo",
                               count_date_start=datetime.now(), count_date_finish=datetime.now(),
                               created_at=datetime.now(), updated_at=datetime.now())
    product = Product(name="Test Product", unit_cost=100, 
                      measure_unit=measure_unit,
                      category=category, cyclic_counts=[cyclic_count],
                      created_at=datetime.now(), updated_at=datetime.now())

    db.add(product)
    db.add(cyclic_count)
    db.commit()

    count_registry = CountRegistry(
        registry_type="system",
        registry_units=100,
        registry_cost=5000,
        difference_units=5,
        difference_cost=250,
        product=product,
        cyclic_count=cyclic_count,
        created_at=datetime.now(), 
        updated_at=datetime.now()
    )
    count_registry_alt = CountRegistry(
        registry_type="system",
        registry_units=100,
        registry_cost=5000,
        difference_units=5,
        difference_cost=250,
        product=product,
        cyclic_count=cyclic_count,
        created_at=datetime.now(), 
        updated_at=datetime.now()
    )
    
    db.add(count_registry)
    db.add(count_registry_alt)
    db.commit()
    
    activity_registry = ActivityRegistry(
        detail="Detail",
        commentary="Commentary",
        user=str(uuid4()),
        count_registry=count_registry_alt,
        created_at=datetime.now(), 
        updated_at=datetime.now()
    )

    db.add(activity_registry)
    db.commit()
    return {
        "product_id": product.id,
        "cyclic_count_id": cyclic_count.id,
        "count_registry_id": count_registry.id,
        "alt_count_registry_id": count_registry_alt.id,
        "activity_registry": activity_registry.id
    }

@pytest.fixture(scope="module")
def setup_database():
    # Crea todas las tablas antes de ejecutar las pruebas
    Base.metadata.create_all(bind=engine)
    yield
    # Elimina todas las tablas después de ejecutar las pruebas
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def db(setup_database):
    # Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def client(setup_database):
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_session] = override_get_db
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
