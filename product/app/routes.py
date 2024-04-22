from datetime import datetime
from fastapi import APIRouter, status, Depends, Header
from app.models import Product
from app.dependencies import is_user_authorized, get_db
from fastapi.exceptions import HTTPException
from app.exceptions import UnauthorizedProductAccessException
from app.schemas import CreateProductModel, UpdateProductModel, ProductResponseModel
from typing import List

from app.exceptions import UserNotFoundException, ProductNotFoundException, InvalidPriceValueException, \
    UnauthorizedProductAccessException, PermissionDeniedException
from app.db import Session

product_router = APIRouter(
    prefix=''
)


@product_router.get('/{product_id}', status_code=status.HTTP_200_OK)
def get_product_by_id(
        product_id: int,
        session: Session = Depends(get_db)
):
    product = session.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found. "
        )

    return product


@product_router.get('/all/', status_code=status.HTTP_200_OK)
def get_all_products(
        session: Session = Depends(get_db)
):
    products = session.query(Product).all()
    return [
        {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "quantity_available": product.quantity_available,
            "user_id": product.user_id
        } for product in products
    ]


@product_router.get('/my-products/', status_code=status.HTTP_200_OK)
def get_my_products(
        user: dict = Depends(is_user_authorized),
        session: Session = Depends(get_db)
):
    if user['role'] != "seller":
        raise PermissionDeniedException()

    my_products = session.query(Product).filter(Product.user_id == user['user_id'])

    return [
        {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price, "quantity_available": product.quantity_available
        } for product in my_products
    ]


@product_router.post('/new-product', response_model=ProductResponseModel, status_code=status.HTTP_201_CREATED)
def create_product(
        product_data: CreateProductModel,
        user: dict = Depends(is_user_authorized),
        session: Session = Depends(get_db)
):
    new_product = Product(
        name=product_data.name,
        description=product_data.description,
        price=product_data.price,
        quantity_available=product_data.quantity_available,
        user_id=user['user_id'],
        created_at=datetime.now()
    )

    session.add(new_product)
    session.commit()
    session.refresh(new_product)

    return new_product


@product_router.patch('/{product_id}', response_model=ProductResponseModel, status_code=status.HTTP_201_CREATED)
def update_product(
        product_id: int,
        product_data: UpdateProductModel,
        user: dict = Depends(is_user_authorized),
        session: Session = Depends(get_db)
):
    if user['role'] != "seller":
        raise PermissionDeniedException()

    product = session.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found. "
        )
    if product.user_id != user['user_id']:
        raise UnauthorizedProductAccessException()

    for attr, value in product_data.dict().items():
        if value is not None:
            setattr(product, attr, value)

    session.add(product)
    session.commit()
    session.refresh(product)

    return product


@product_router.delete('/{product_id}', status_code=status.HTTP_201_CREATED)
def delete_product(
        product_id: int,
        user: dict = Depends(is_user_authorized),
        session: Session = Depends(get_db)
):
    if user['role'] == "buyer":
        raise PermissionDeniedException()

    product = session.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found. "
        )
    if user['role'] == "seller" and product.user_id != user['user_id']:
        raise UnauthorizedProductAccessException()

    session.delete(product)
    session.commit()

    return {
        "message": "Product deleted successfully."
    }
