from uuid import uuid4
from app import schemas

###############Warehouse
def test_create_warehouse(client, sample_data_warehouse):
    response = client.post(
        "/warehouses/",
        json={
            "name": "New Warehouse",
            "country": "Peru",
            "state": "Lima",
            "city": "Lima",
            "address": "Av BBB y Calle BBB, Edificio BBB",
            "company_id": str(uuid4()),
            "warehouse_type_id": str(sample_data_warehouse["warehouse_type_id"])
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "New Warehouse"
    assert data["country"] == "Peru"

def test_read_warehouses(client):
    response = client.get("/warehouses/")
    assert response.status_code == 200
    data = response.json()
    result = schemas.PaginatedResource(**data)
    assert result is not None

def test_update_warehouse(client, sample_data_warehouse):
    warehouse_id = str(sample_data_warehouse["warehouse_id"])
    response = client.put(
        f"/warehouses/{warehouse_id}",
        json={"name": "Updated Warehouse"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Warehouse"

def test_delete_warehouse(client, sample_data_warehouse):
    #First fetch locations
    warehouse_id = str(sample_data_warehouse["warehouse_id"])
    response = client.get(f"/warehouses/{warehouse_id}")
    data = response.json()
    wh_locations = data["wh_locations"]
    for location in wh_locations:
        client.delete(f"whlocations/{location['id']}")
    #Then Delete
    response = client.delete(f"/warehouses/{warehouse_id}")
    assert response.status_code == 200
    
##################Warehouse Type 

def test_create_warehouse_type(client):
    response = client.post(
        "/warehouse_types/",
        json={"name": "Type B", "description": "Type B Description"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Type B"
    assert data["description"] == "Type B Description"

def test_read_warehouse_types(client):
    response = client.get("/warehouse_types/")
    assert response.status_code == 200
    data = response.json()
    result = schemas.PaginatedResource(**data)
    assert result is not None

def test_update_warehouse_type(client, sample_data_warehouse):
    warehouse_type_id = str(sample_data_warehouse["warehouse_type_id"])
    response = client.put(
        f"/warehouse_types/{warehouse_type_id}",
        json={"name": "Updated Type"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Type"

def test_delete_warehouse_type(client, sample_data_warehouse):
    #Fetch warehouses of type first
    warehouse_type_id = str(sample_data_warehouse["warehouse_type_id"])
    response = client.get(f"/warehouse_types/{warehouse_type_id}")
    data = response.json()
    warehouses = data["warehouses"]
    for warehouse in warehouses:
        client.delete(f"warehouses/{warehouse['id']}")
    #Then delete
    response = client.delete(f"/warehouse_types/{warehouse_type_id}")
    assert response.status_code == 200
    data = response.json()

########################Warehouse Locations
def test_create_wh_location(client, sample_data_warehouse):
    response = client.post(
        "/whlocations/",
        json={
            "name": "Shelf 2",
            "description": "Second shelf",
            "wh_location_type_id": str(sample_data_warehouse["wh_location_type_id"]),
            "warehouse_id": str(sample_data_warehouse["alt_warehouse_id"])
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Shelf 2"
    assert data["description"] == "Second shelf"

def test_read_wh_locations(client):
    response = client.get("/whlocations/")
    assert response.status_code == 200
    data = response.json()
    result = schemas.PaginatedResource(**data)
    assert result is not None

def test_update_wh_location(client, sample_data_warehouse):
    wh_location_id = str(sample_data_warehouse["wh_location_id"])
    response = client.put(
        f"/whlocations/{wh_location_id}",
        json={"name": "Updated Shelf"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Shelf"

def test_delete_wh_location(client, sample_data_warehouse):
    wh_location_id = str(sample_data_warehouse["wh_location_id"])
    response = client.delete(f"/whlocations/{wh_location_id}")
    assert response.status_code == 200
    data = response.json()

#################WH_LOCATION_TYPE
def test_create_wh_location_type(client):
    response = client.post(
        "/whlocation_types/",
        json={"name": "Pallet"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Pallet"

def test_read_wh_location_types(client):
    response = client.get("/whlocation_types/")
    assert response.status_code == 200
    data = response.json()
    result = schemas.PaginatedResource(**data)
    assert result is not None

def test_update_wh_location_type(client, sample_data_warehouse):
    wh_location_type_id = str(sample_data_warehouse["wh_location_type_id"])
    response = client.put(
        f"/whlocation_types/{wh_location_type_id}",
        json={"name": "Updated Type"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Type"

def test_delete_wh_location_type(client, sample_data_warehouse):
    wh_location_type_id = str(sample_data_warehouse["wh_location_type_id"])
    response = client.delete(f"/whlocation_types/{wh_location_type_id}")
    assert response.status_code == 200
    data = response.json()

#######################PRODUCT
def test_create_product(client, sample_product_data):
    category_id = sample_product_data["category_id"]
    measure_unit_id = sample_product_data["measure_unit_id"]
    response = client.post("/products/", json={
        "name": "Product 1",
        "code": "P001",
        "sku": "SKU001",
        "unit_cost": 10000,
        "measure_unit_id": str(measure_unit_id),
        "category_id": str(category_id)
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Product 1"

def test_read_products(client) -> None:
    response = client.get("/products/")
    assert response.status_code == 200
    data = response.json()
    result = schemas.PaginatedResource(**data)
    assert result is not None

def test_update_product(client, sample_product_data):
    product_id = sample_product_data["product_id"]
    response = client.put(f"/products/{str(product_id)}", json={
        "name": "Updated Product"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Product"

def test_delete_product(client, sample_product_data):
    
    product_id = sample_product_data["product_id"]
    response = client.delete(f"/products/{str(product_id)}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(product_id)

#######################PRODUCT CATEGORY
def test_create_product_category(client):
    response = client.post("/product_categories/", json={
        "name": "Category 1",
        "short_codename": "CAT1"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Category 1"

def test_read_product_categories(client) -> None:
    response = client.get("/product_categories/")
    assert response.status_code == 200
    data = response.json()
    result = schemas.PaginatedResource(**data)
    assert result is not None

def test_update_product_category(client, sample_product_category_mu_data):
    category_id = sample_product_category_mu_data["category_id"]
    response = client.put(f"/product_categories/{category_id}", json={
        "name": "Updated Product"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Product"

def test_delete_product_category(client, sample_product_category_mu_data):
    category_id = sample_product_category_mu_data["category_id"]
    response = client.delete(f"/product_categories/{str(category_id)}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(category_id)

#######################Measure Unit
def test_create_measure_unit(client):
    response = client.post("/measure_units/", json={
        "name": "Unidades",
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Unidades"

def test_read_measure_units(client) -> None:
    response = client.get("/measure_units/")
    assert response.status_code == 200
    data = response.json()
    result = schemas.PaginatedResource(**data)
    assert result is not None

def test_update_measure_unit(client, sample_product_category_mu_data):
    measure_unit_id = sample_product_category_mu_data["measure_unit_id"]
    response = client.put(f"/measure_units/{measure_unit_id}", json={
        "name": "Updated Unit"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Unit"

def test_delete_measure_unit(client, sample_product_category_mu_data):
    measure_unit_id = sample_product_category_mu_data["measure_unit_id"]
    response = client.delete(f"/measure_units/{str(measure_unit_id)}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(measure_unit_id)
