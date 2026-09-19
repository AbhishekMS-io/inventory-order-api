# Inventory & Order Management API

A RESTful backend API for managing products, inventory, and customer orders.

This project was developed as a Backend Developer technical assignment using **FastAPI, PostgreSQL, SQLAlchemy, and Pydantic**.

---

## Tech Stack

- **Python 3.10+**
- **FastAPI** – REST API framework
- **PostgreSQL** – Relational database
- **SQLAlchemy** – ORM
- **Pydantic** – Request/response validation
- **Uvicorn** – ASGI server
- **Pytest** – Automated testing
- **HTTPX** – API testing

---

## Features

### Product Management

- Create a product
- List all products
- Get a product by ID
- Update a product
- Delete a product
- Prevent duplicate SKUs
- Validate product data

### Order Management

- Create orders containing one or more products
- Validate product availability
- Validate order quantities
- Calculate order total on the backend
- Automatically reduce inventory after a successful order
- Store the product price at the time of purchase
- Get an order by ID
- List all orders
- Handle invalid and unavailable products

### API Features

- RESTful API design
- Proper HTTP status codes
- Input validation
- Error handling
- Database transaction handling
- Swagger/OpenAPI documentation
- Automated tests
- Environment-based database configuration

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
```

---

# Requirements

Make sure the following are installed:

- Python 3.10+
- PostgreSQL
- pip
- Git

The project can be run on:

- Windows
- Linux
- WSL2
- macOS

---

# Installation

## 1. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd inventory-order-api
```

Replace `<YOUR_GITHUB_REPOSITORY_URL>` with the actual GitHub repository URL.

---

## 2. Create a Virtual Environment

### Windows PowerShell

```powershell
python -m venv venv
venv\Scripts\activate
```

### Windows Command Prompt

```cmd
python -m venv venv
venv\Scripts\activate
```

### Linux / WSL / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# PostgreSQL Configuration

The application uses PostgreSQL as its database.

Make sure PostgreSQL is installed and running before starting the API.

## Create Database and User

Open PostgreSQL using `psql` or pgAdmin.

Create the database:

```sql
CREATE DATABASE inventory_db;
```

Create the application user:

```sql
CREATE USER inventory_user WITH PASSWORD 'inventory_password';
```

Grant database privileges:

```sql
GRANT ALL PRIVILEGES ON DATABASE inventory_db TO inventory_user;
```

Connect to the database:

```sql
\c inventory_db
```

Grant schema privileges:

```sql
GRANT USAGE, CREATE ON SCHEMA public TO inventory_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO inventory_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO inventory_user;
```

> You can use a different PostgreSQL username/password if preferred. Update the `DATABASE_URL` accordingly.

---

# Environment Configuration

Create a `.env` file in the project root.

```env
DATABASE_URL=postgresql://inventory_user:inventory_password@localhost:5432/inventory_db
```

A `.env.example` file is included in the repository:

```env
DATABASE_URL=postgresql://inventory_user:your_password@localhost:5432/inventory_db
```

### Important

Do not commit the `.env` file to Git because it contains database credentials.

---

# Running the Application

Start the FastAPI development server:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

---

# API Documentation

FastAPI automatically generates interactive API documentation.

## Swagger UI

Open:

```text
http://127.0.0.1:8000/docs
```

Swagger allows you to:

- View all endpoints
- View request schemas
- View response schemas
- Send API requests
- Test validation
- Test error responses

## ReDoc

Open:

```text
http://127.0.0.1:8000/redoc
```

---

# API Endpoints

## Product Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/products` | Create a product |
| GET | `/products` | List all products |
| GET | `/products/{product_id}` | Get a product |
| PUT | `/products/{product_id}` | Update a product |
| DELETE | `/products/{product_id}` | Delete a product |

## Order Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/orders` | Create an order |
| GET | `/orders` | List all orders |
| GET | `/orders/{order_id}` | Get an order |

## Health Check

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Check API status |

---

# Product API

## Create Product

### Request

```http
POST /products
```

Example request body:

```json
{
  "name": "Wireless Mouse",
  "sku": "WM-001",
  "description": "Wireless optical mouse",
  "price": 799.99,
  "available_quantity": 50
}
```

Example response:

```json
{
  "id": 1,
  "name": "Wireless Mouse",
  "sku": "WM-001",
  "description": "Wireless optical mouse",
  "price": 799.99,
  "available_quantity": 50
}
```

---

## List Products

```http
GET /products
```

Example response:

```json
[
  {
    "id": 1,
    "name": "Wireless Mouse",
    "sku": "WM-001",
    "description": "Wireless optical mouse",
    "price": 799.99,
    "available_quantity": 50
  }
]
```

---

## Get Product

```http
GET /products/1
```

Returns the product with ID `1`.

If the product does not exist:

```json
{
  "detail": "Product not found"
}
```

Response status:

```text
404 Not Found
```

---

## Update Product

```http
PUT /products/1
```

Example request:

```json
{
  "name": "Wireless Mouse Pro",
  "sku": "WM-001",
  "description": "Updated wireless mouse",
  "price": 999.99,
  "available_quantity": 75
}
```

---

## Delete Product

```http
DELETE /products/1
```

If successful:

```text
204 No Content
```

---

# Order API

## Create Order

An order must contain one or more products and quantities.

```http
POST /orders
```

Example request:

```json
{
  "items": [
    {
      "product_id": 1,
      "quantity": 2
    },
    {
      "product_id": 2,
      "quantity": 1
    }
  ]
}
```

When an order is created, the backend:

1. Validates the products.
2. Checks inventory availability.
3. Calculates the order total.
4. Stores the order.
5. Stores each product's unit price at purchase time.
6. Reduces the available inventory.

The client does not provide the order total.

---

## Example Order Response

```json
{
  "id": 1,
  "total_amount": 2599.97,
  "created_at": "2026-09-19T10:30:00Z",
  "items": [
    {
      "product_id": 1,
      "product_name": "Wireless Mouse",
      "quantity": 2,
      "unit_price": 799.99,
      "subtotal": 1599.98
    },
    {
      "product_id": 2,
      "product_name": "Keyboard",
      "quantity": 1,
      "unit_price": 999.99,
      "subtotal": 999.99
    }
  ]
}
```

The order total is calculated by the backend.

---

# Inventory Handling

When an order is successfully created, the ordered quantity is deducted from the product inventory.

Example:

```text
Initial inventory:       10
Quantity ordered:         3
Remaining inventory:      7
```

If there is insufficient inventory, the order is rejected and the inventory is not reduced.

Example:

```text
Available quantity:       2
Requested quantity:       5
```

Response:

```json
{
  "detail": "Insufficient inventory for product ID 1"
}
```

Response status:

```text
400 Bad Request
```

---

# Validation and Error Handling

The API uses Pydantic validation and appropriate HTTP status codes.

## Common Status Codes

| Status Code | Meaning |
|---|---|
| `200 OK` | Successful request |
| `201 Created` | Resource successfully created |
| `204 No Content` | Resource successfully deleted |
| `400 Bad Request` | Invalid business operation |
| `404 Not Found` | Resource does not exist |
| `409 Conflict` | Duplicate SKU |
| `422 Unprocessable Entity` | Request validation error |

---

## Duplicate SKU

SKUs must be unique.

Trying to create another product with an existing SKU returns:

```text
409 Conflict
```

Example:

```json
{
  "detail": "SKU already exists"
}
```

---

## Invalid Quantity

Product and order quantities must be valid positive values.

For example:

```json
{
  "quantity": 0
}
```

will be rejected by request validation.

---

## Empty Order

An order must contain at least one item.

Example:

```json
{
  "items": []
}
```

is rejected.

---

## Duplicate Products in an Order

The same product cannot be added multiple times within a single order.

Example:

```json
{
  "items": [
    {
      "product_id": 1,
      "quantity": 2
    },
    {
      "product_id": 1,
      "quantity": 3
    }
  ]
}
```

is rejected.

---

# Database Design

The application uses PostgreSQL with SQLAlchemy ORM.

## Products

The products table contains:

- `id`
- `name`
- `sku`
- `description`
- `price`
- `available_quantity`

The `sku` field is unique.

## Orders

The orders table contains:

- `id`
- `total_amount`
- `created_at`

## Order Items

The order items table contains:

- `id`
- `order_id`
- `product_id`
- `quantity`
- `unit_price`

The `unit_price` is stored when the order is created so historical orders retain the price at the time of purchase.

---

# Transaction Handling

Order creation performs the required database operations together:

1. Validate products.
2. Check inventory.
3. Calculate the order total.
4. Create the order.
5. Create order items.
6. Reduce inventory.
7. Commit the transaction.

If an error occurs during the operation, the transaction is rolled back.

This helps prevent partially completed orders.

---

# Testing

The project includes automated tests using **Pytest**.

Run the test suite:

```bash
pytest
```

The tests cover:

- Product creation
- Product listing
- Product retrieval
- Product update
- Product deletion
- Duplicate SKU validation
- Invalid product data
- Order creation
- Order total calculation
- Inventory reduction
- Insufficient inventory
- Invalid order quantities
- Non-existent products
- Order retrieval
- Order listing

Expected result:

```text
13 passed
```

> The exact number of tests may change if additional tests are added.

---

# Test Database

The automated tests use a separate PostgreSQL database so testing does not modify the main application database.

Example test database:

```text
inventory_test_db
```

Configure the test database using:

```env
TEST_DATABASE_URL=postgresql://inventory_user:your_password@localhost:5432/inventory_test_db
```

Make sure the test database exists before running the test suite.

---

# Running on Windows

The project can be run directly on Windows without WSL.

## 1. Clone the repository

```powershell
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd inventory-order-api
```

## 2. Create virtual environment

```powershell
python -m venv venv
venv\Scripts\activate
```

## 3. Install dependencies

```powershell
pip install -r requirements.txt
```

## 4. Configure PostgreSQL

Create the PostgreSQL database and user as described in the PostgreSQL Configuration section.

Create a `.env` file:

```env
DATABASE_URL=postgresql://inventory_user:inventory_password@localhost:5432/inventory_db
```

## 5. Run the API

```powershell
uvicorn app.main:app --reload
```

## 6. Open Swagger

Open the following in a browser:

```text
http://127.0.0.1:8000/docs
```

---

# Running on Linux / WSL2

The project can also be run using WSL2 with Ubuntu.

Start PostgreSQL:

```bash
sudo service postgresql start
```

Activate the virtual environment:

```bash
source venv/bin/activate
```

Run the API:

```bash
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

---

# Example API Workflow

A typical inventory and order workflow is:

```text
Create Product
      |
      v
Check Product Inventory
      |
      v
Create Order
      |
      v
Validate Product Availability
      |
      v
Calculate Order Total
      |
      v
Reduce Inventory
      |
      v
Save Order
      |
      v
Return Order Details
```

---

# Testing with Swagger

After starting the API:

```bash
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

A basic test flow is:

### Step 1 — Create a product

Use:

```text
POST /products
```

Example:

```json
{
  "name": "Keyboard",
  "sku": "KB-001",
  "description": "Mechanical keyboard",
  "price": 1499.99,
  "available_quantity": 20
}
```

### Step 2 — Check products

Use:

```text
GET /products
```

Verify the product exists.

### Step 3 — Create an order

Use:

```text
POST /orders
```

Example:

```json
{
  "items": [
    {
      "product_id": 1,
      "quantity": 2
    }
  ]
}
```

### Step 4 — Verify inventory

Use:

```text
GET /products/1
```

The available quantity should have decreased by `2`.

### Step 5 — Verify the order

Use:

```text
GET /orders/1
```

Verify that:

- The order exists.
- The total was calculated by the backend.
- The product quantity is correct.
- The unit price was stored.

---

# Security

Sensitive configuration such as database credentials is stored using environment variables.

The following files/directories are excluded from Git:

```text
.env
venv/
__pycache__/
.pytest_cache/
*.py[cod]
```

Only `.env.example` is included in the repository.

---

# Design Decisions

### FastAPI

FastAPI was selected because it provides:

- Automatic OpenAPI documentation
- Request validation
- Clear API structure
- High performance
- Easy integration with SQLAlchemy

### PostgreSQL

PostgreSQL was selected as the relational database because the project requires structured relationships between products, orders, and order items.

### SQLAlchemy

SQLAlchemy provides ORM support and keeps database operations organized within the application.

### Pydantic

Pydantic is used to validate API request and response data.

---

# Project Goals

The main goals of this project are:

- Build a clean REST API
- Implement proper database handling
- Validate user input
- Keep business logic on the backend
- Maintain inventory consistency
- Provide clear API documentation
- Write automated tests
- Follow a maintainable project structure
- Support both Windows and Linux/WSL development environments

---

# License

This project was developed as a technical assignment for evaluation purposes.

---

# Author

**Abhishek MS**

Backend Developer Technical Assignment
