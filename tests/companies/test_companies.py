from fastapi.testclient import TestClient

##################CONTACT TEST
def test_create_contact(client: TestClient, sample_companies_data):
    company_id = str(sample_companies_data["company_id"])
    contact_data = {
        "full_name": "John Doe",
        "contact_number": "123456789",
        "alt_contact_number": "987654321",
        "employee_charge": "Manager",
        "email": "john.doe@company.com",
        "company_id": str(company_id)
    }
    response = client.post("/contacts/", json=contact_data)
    assert response.status_code == 200
    assert response.json()["full_name"] == "John Doe"

def test_read_contacts(client: TestClient, sample_companies_data):
    response = client.get("/contacts/")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_update_contact(client: TestClient, sample_companies_data):
    contact_id = sample_companies_data["contact_id"]

    update_data = {
        "full_name": "Jane Doe",
        "email": "jane.doe@company.com"
    }
    response = client.put(f"/contacts/{str(contact_id)}", json=update_data)
    assert response.status_code == 200
    assert response.json()["full_name"] == "Jane Doe"
    assert response.json()["email"] == "jane.doe@company.com"

def test_delete_contact(client: TestClient, sample_companies_data):
    contact_id= sample_companies_data["contact_id"]

    response = client.delete(f"/contacts/{str(contact_id)}")
    assert response.status_code == 200
    assert response.json()["id"] == str(contact_id)


##################COMPANY TEST
def test_create_companies(client: TestClient, sample_companies_data):
    corp_group_id = str(sample_companies_data["corp_group_id"])
    company_data = {
        "name": "Compania AAA",
        "codename": "CMY-AAA",
        "phone_number": "123456789",
        "cellphone_number": "987654321",
        "email": "contact@companiaaaa.com",
        "ruc": "1234567890",
        "foundation_date": "2020-01-01",
        "corporate_group_id": str(corp_group_id)
    }
    response = client.post("/companies/", json=company_data)
    assert response.status_code == 200
    assert response.json()["name"] == "Compania AAA"

def test_read_companies(client: TestClient):
    response = client.get("/companies/")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_update_company(client: TestClient, sample_companies_data):
    company_id = sample_companies_data["company_id"]

    update_data = {
        "name": "Compania Actualizada",
        "email": "newcontact@companiaaaa.com"
    }
    response = client.put(f"/companies/{str(company_id)}", json=update_data)
    assert response.status_code == 200
    assert response.json()["name"] == "Compania Actualizada"
    assert response.json()["email"] == "newcontact@companiaaaa.com"

def test_delete_company(client: TestClient, sample_companies_data):
    #Fetch contacts
    company_id= sample_companies_data["company_id"]
    response = client.get(f"/companies/{company_id}")
    data = response.json()
    contacts = data["contacts"]
    for contact in contacts:
        client.delete(f"contacts/{contact['id']}")
    #Then delete
    response = client.delete(f"/companies/{str(company_id)}")
    assert response.status_code == 200
    assert response.json()["id"] == str(company_id)


##################CORPORATE GROUP TEST
def test_create_group(client: TestClient, sample_companies_data):
    group_data = {
        "name": "Grupo Corporativo",
        "description": "Descripción del grupo"
    }
    response = client.post("/corporative_groups/", json=group_data)
    assert response.status_code == 200
    assert response.json()["name"] == "Grupo Corporativo"

def test_read_groups(client: TestClient):
    response = client.get("/corporative_groups/")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_update_group(client: TestClient, sample_companies_data):
    corp_group_id = sample_companies_data["corp_group_id"]
    update_data = {
        "name": "Grupo Corporativo Actualizado"
    }
    response = client.put(f"/corporative_groups/{str(corp_group_id)}", json=update_data)
    assert response.status_code == 200
    assert response.json()["name"] == "Grupo Corporativo Actualizado"

def test_delete_group(client: TestClient, sample_companies_data):
    #Fetch contacts
    corp_group_id= sample_companies_data["corp_group_id"]
    response = client.get(f"/corporative_groups/{corp_group_id}")
    data = response.json()
    companies = data["companies"]
    for company in companies:
        client.delete(f"companies/{company['id']}")
    #Then delete
    response = client.delete(f"/corporative_groups/{str(corp_group_id)}")
    assert response.status_code == 200
    assert response.json()["id"] == str(corp_group_id)

