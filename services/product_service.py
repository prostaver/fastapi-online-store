from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models import product as model_product
from py_schemas import product as product_schema


def create_product(db: Session, product_input: product_schema.CreateProduct):
    product_data = model_product.Product(
        product_input.name, product_input.description, product_input.price
    )

    db.add(product_data)
    db.commit()

    print(product_data)
    return product_data


def update_product(
    db: Session, product_input: product_schema.CreateProduct, product_id: int
):
    product_data = (
        db.query(model_product.Product)
        .filter(model_product.Product.id == product_id)
        .first()
    )

    if not product_data:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            f"No product found with id: {product_id}",
        )

    product_data.name = product_input.name
    product_data.description = product_input.description
    product_data.price = product_input.price

    db.add(product_data)
    db.commit()

    print(product_data)
    return product_data


def get_products(db: Session):
    return db.query(model_product.Product).all()


def get_product(db: Session, product_id: int):
    product = (
        db.query(model_product.Product)
        .filter(model_product.Product.id == product_id)
        .first()
    )
    if not product:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            f"No product found with id: {product_id}",
        )
    return product


def delete_product(db: Session, product_id: int):
    product = (
        db.query(model_product.Product)
        .filter(model_product.Product.id == product_id)
        .first()
    )
    if not product:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            f"No product found with id: {product_id}",
        )

    db.delete(product)
    db.commit()

    print(type({"message": f"Successfully deleted user with id {product_id}"}))
    return {"message": f"Successfully deleted user with id {product_id}"}


def calculate_amount(db: Session, product_id: int, quantity: int) -> Decimal:
    product = (
        db.query(model_product.Product)
        .filter(model_product.Product.id == product_id)
        .first()
    )

    return product.price * quantity
