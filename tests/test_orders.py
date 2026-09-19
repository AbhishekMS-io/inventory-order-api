def test_create_order(client):
    product_response = client.post(
        "/products",
        json={
            "name": "Test Mouse",
            "sku": "ORDER-001",
            "description": "Mouse for order testing",
            "price": 500,
            "available_quantity": 10
        }
    )

    product_id = product_response.json()["id"]

    response = client.post(
        "/orders",
        json={
            "items": [
                {
                    "product_id": product_id,
                    "quantity": 2
                }
            ]
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["total_amount"] == "1000.00"
    assert data["items"][0]["quantity"] == 2




def test_inventory_reduction(client):
    product_response = client.post(
        "/products",
        json={
            "name": "Inventory Test",
            "sku": "STOCK-001",
            "description": "Stock testing",
            "price": 100,
            "available_quantity": 10
        }
    )

    product_id = product_response.json()["id"]

    order_response = client.post(
        "/orders",
        json={
            "items": [
                {
                    "product_id": product_id,
                    "quantity": 3
                }
            ]
        }
    )

    assert order_response.status_code == 201

    product_response = client.get(
        f"/products/{product_id}"
    )

    assert product_response.json()["available_quantity"] == 7





def test_insufficient_inventory(client):
    product_response = client.post(
        "/products",
        json={
            "name": "Limited Stock",
            "sku": "LIMITED-001",
            "description": "Limited stock product",
            "price": 100,
            "available_quantity": 2
        }
    )

    product_id = product_response.json()["id"]

    response = client.post(
        "/orders",
        json={
            "items": [
                {
                    "product_id": product_id,
                    "quantity": 5
                }
            ]
        }
    )

    assert response.status_code == 400

    product_response = client.get(
        f"/products/{product_id}"
    )

    assert product_response.json()["available_quantity"] == 2






def test_multiple_products_order(client):
    mouse = client.post(
        "/products",
        json={
            "name": "Mouse",
            "sku": "MULTI-MOUSE",
            "description": "Mouse",
            "price": 500,
            "available_quantity": 10
        }
    ).json()

    keyboard = client.post(
        "/products",
        json={
            "name": "Keyboard",
            "sku": "MULTI-KEYBOARD",
            "description": "Keyboard",
            "price": 1000,
            "available_quantity": 10
        }
    ).json()

    response = client.post(
        "/orders",
        json={
            "items": [
                {
                    "product_id": mouse["id"],
                    "quantity": 2
                },
                {
                    "product_id": keyboard["id"],
                    "quantity": 1
                }
            ]
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["total_amount"] == "2000.00"
    assert len(data["items"]) == 2





def test_order_with_nonexistent_product(client):
    response = client.post(
        "/orders",
        json={
            "items": [
                {
                    "product_id": 99999,
                    "quantity": 1
                }
            ]
        }
    )

    assert response.status_code == 404






def test_invalid_order_quantity(client):
    response = client.post(
        "/orders",
        json={
            "items": [
                {
                    "product_id": 1,
                    "quantity": 0
                }
            ]
        }
    )

    assert response.status_code == 422