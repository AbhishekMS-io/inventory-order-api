def test_create_product(client):
    response = client.post(
        "/products",
        json={
            "name": "Wireless Mouse",
            "sku": "WM-TEST-001",
            "description": "Wireless mouse",
            "price": 799.99,
            "available_quantity": 20
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Wireless Mouse"
    assert data["sku"] == "WM-TEST-001"
    assert data["available_quantity"] == 20





def test_duplicate_sku(client):
    product = {
        "name": "Wireless Mouse",
        "sku": "DUPLICATE-001",
        "description": "Mouse",
        "price": 500,
        "available_quantity": 10
    }

    first_response = client.post(
        "/products",
        json=product
    )

    assert first_response.status_code == 201

    second_response = client.post(
        "/products",
        json=product
    )

    assert second_response.status_code == 409






def test_get_products(client):
    client.post(
        "/products",
        json={
            "name": "Keyboard",
            "sku": "KB-TEST-001",
            "description": "Mechanical keyboard",
            "price": 2500,
            "available_quantity": 15
        }
    )

    response = client.get("/products")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["sku"] == "KB-TEST-001"




def test_get_nonexistent_product(client):
    response = client.get("/products/99999")

    assert response.status_code == 404



def test_invalid_product(client):
    response = client.post(
        "/products",
        json={
            "name": "",
            "sku": "",
            "description": "Invalid product",
            "price": -100,
            "available_quantity": -5
        }
    )

    assert response.status_code == 422




def test_update_product(client):
    create_response = client.post(
        "/products",
        json={
            "name": "Old Mouse",
            "sku": "UPDATE-001",
            "description": "Old description",
            "price": 500,
            "available_quantity": 10
        }
    )

    product_id = create_response.json()["id"]

    response = client.put(
        f"/products/{product_id}",
        json={
            "name": "New Mouse",
            "price": 750
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "New Mouse"
    assert float(data["price"]) == 750





def test_delete_product(client):
    create_response = client.post(
        "/products",
        json={
            "name": "Delete Me",
            "sku": "DELETE-001",
            "description": "Temporary product",
            "price": 100,
            "available_quantity": 5
        }
    )

    product_id = create_response.json()["id"]

    response = client.delete(
        f"/products/{product_id}"
    )

    assert response.status_code == 204

    get_response = client.get(
        f"/products/{product_id}"
    )

    assert get_response.status_code == 404