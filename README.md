# Inventory & Order Management API

A RESTful backend API for managing products, inventory, and orders.

## Tech Stack

- Python 3.12
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- Pytest
- Uvicorn

## Features

### Product Management

- Create products
- List products
- Get product by ID
- Update products
- Delete products
- Prevent duplicate SKUs
- Validate product data

### Order Management

- Create orders containing one or more products
- Validate product availability
- Calculate order total on the backend
- Automatically reduce inventory
- Store unit price at the time of order
- Get order by ID
- List all orders
- Handle insufficient inventory
- Database transaction handling

### Additional

- PostgreSQL database
- Swagger/OpenAPI documentation
- Request validation
- Appropriate HTTP status codes
- Error handling
- Automated tests

---

## Project Structure

```text
inventory-order-api/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── product.py
│   │   └── order.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── product.py
│   │   └── order.py
│   │
│   └── routers/
│       ├── __init__.py
│       ├── products.py
│       └── orders.py
│
├── tests/
│   ├── conftest.py
│   ├── test_products.py
│   └── test_orders.py
│
├── .env.example
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md



Requirements:

Python 3.12+
PostgreSQL
Git
pip

The project was developed and tested using WSL2 with Ubuntu.
