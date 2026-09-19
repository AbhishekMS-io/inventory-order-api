from decimal import Decimal

from pydantic import BaseModel, Field, ConfigDict


class ProductCreate(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        max_length=100
    )

    sku: str = Field(
        ...,
        min_length=1,
        max_length=50
    )

    description: str | None = None

    price: Decimal = Field(
        ...,
        gt=0
    )

    available_quantity: int = Field(
        ...,
        ge=0
    )


class ProductUpdate(BaseModel):
    name: str | None = Field(
        None,
        min_length=1,
        max_length=100
    )

    sku: str | None = Field(
        None,
        min_length=1,
        max_length=50
    )

    description: str | None = None

    price: Decimal | None = Field(
        None,
        gt=0
    )

    available_quantity: int | None = Field(
        None,
        ge=0
    )


class ProductResponse(BaseModel):
    id: int
    name: str
    sku: str
    description: str | None
    price: Decimal
    available_quantity: int

    model_config = ConfigDict(
        from_attributes=True
    )