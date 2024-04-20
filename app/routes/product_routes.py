from datetime import datetime
from fastapi import APIRouter, status, Depends
from app.models import User, Product
from app.schemas import CreateProductModel, UpdateProductModel, ProductResponseModel
from app.exceptions import ProductNotFoundException, InvalidPriceValueException, UnauthorizedProductAccessException
from app.db import Session
from app.dependencies import get_db, can_post_product

product_router = APIRouter(
    prefix='/product',
    tags=['product']
)


@product_router.get('/', status_code=status.HTTP_201_CREATED)
def get_all_products(session: Session = Depends(get_db)):
    products = session.query(Product).all()
    return products


@product_router.get('/{product_id}', response_model=ProductResponseModel, status_code=status.HTTP_200_OK)
def get_product_by_id(
        product_id: int,
        session: Session = Depends(get_db)
):
    product = session.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise ProductNotFoundException(product_id)

    return product


@product_router.post('/', response_model=CreateProductModel, status_code=status.HTTP_201_CREATED)
def create_product(
        product: CreateProductModel,
        session: Session = Depends(get_db),
        user: User = Depends(can_post_product)
):
    if product.price <= 0:
        raise InvalidPriceValueException()

    new_product = Product(
        user_id=user.id,
        name=product.name,
        description=product.description,
        price=product.price,
        created_at=datetime.now()
    )

    session.add(new_product)
    session.commit()
    session.refresh(new_product)

    return new_product

# Check => SCOPES
@product_router.put('/{product_id}', response_model=ProductResponseModel, status_code=status.HTTP_200_OK)
def update_product(
        product_id: int,
        product_data: UpdateProductModel,
        session: Session = Depends(get_db),
        user: User = Depends(can_post_product)
):

    product = session.query(Product).filter(Product.id == product_id).first()

    if product is None:
        raise ProductNotFoundException(product_id)

    if user.id != product.user_id:
        raise UnauthorizedProductAccessException()

    if product_data.name is not None:
        product.name = product_data.name
    if product_data.description is not None:
        product.description = product_data.description
    if product_data.price is not None:
        if product_data.price <= 0:
            raise InvalidPriceValueException()
        product.price = product_data.price

    session.commit()
    session.refresh(product)

    return product


@product_router.delete('/{product_id}', status_code=status.HTTP_200_OK)
def delete_product(
        product_id: int,
        session: Session = Depends(get_db),
        user: User = Depends(can_post_product)
):

    product = session.query(Product).filter(Product.id == product_id).first()

    if product is None:
        raise ProductNotFoundException(product_id)

    if user.id != product.user_id:
        raise UnauthorizedProductAccessException()

    session.delete(product)
    session.commit()

    return {"message": "Product deleted successfully. "}
