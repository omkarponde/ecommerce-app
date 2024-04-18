from fastapi import APIRouter, status, Depends
from app.dependencies import get_db, can_order_product
from app.models import User, Product, Order
from app.schemas import CreateOrderModel, UpdateOrderModel, OrderResponseModel
from app.exceptions import ProductNotFoundException, OrderNotFoundException, MinimumOneProductRequiredException, UnauthorizedOrderAccessException
from app.db import Session
from datetime import datetime

order_router = APIRouter(
    prefix='/order',
    tags=['order']
)


@order_router.get('/', status_code=status.HTTP_200_OK)
async def get_all_orders(session: Session = Depends(get_db)):
    orders = session.query(Order).all()
    return orders


@order_router.get('/{order_id}', response_model=OrderResponseModel, status_code=status.HTTP_200_OK)
async def get_order_by_id(
        order_id: int,
        session: Session = Depends(get_db)
):
    order = session.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise OrderNotFoundException(order_id)
    return order


@order_router.post('/', response_model=OrderResponseModel, status_code=status.HTTP_201_CREATED)
def create_order(
        order: CreateOrderModel,
        session: Session = Depends(get_db),
        user: User = Depends(can_order_product)
):

    if len(order.product_ids) == 0:
        raise MinimumOneProductRequiredException()
    total_cost = 0
    products = []
    for product_id in order.product_ids:
        product = session.query(Product).filter(Product.id == product_id).first()
        products.append(product)
        if not product:
            raise ProductNotFoundException(product_id)

        total_cost += product.price

    new_order = Order(
        user_id=user.id,
        price=total_cost,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    session.add(new_order)
    session.commit()

    for product in products:
        new_order.products.append(product)

    session.commit()

    return new_order


@order_router.put('/{order_id}', response_model=OrderResponseModel, status_code=status.HTTP_200_OK)
def update_order(
        order_id: int,
        order_data: UpdateOrderModel,
        session: Session = Depends(get_db),
        user: User = Depends(can_order_product)
):
    order = session.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise OrderNotFoundException(order_id)

    if order.user_id != user.id:
        raise UnauthorizedOrderAccessException()

    if len(order_data.product_ids) == 0:
        raise MinimumOneProductRequiredException()

    total_cost = 0
    products = []
    for product_id in order_data.product_ids:
        product = session.query(Product).filter(Product.id == product_id).first()
        products.append(product)
        if not product:
            raise ProductNotFoundException(product_id)

        total_cost += product.price

    order.products.clear()
    for product in products:
        order.products.append(product)
    order.price = total_cost
    order.updated_at = datetime.now()

    session.commit()
    session.refresh(order)

    return order


@order_router.delete('/{order_id}', status_code=status.HTTP_200_OK)
def delete_order(
        order_id: int,
        session: Session = Depends(get_db),
        user: User = Depends(can_order_product)
):
    order = session.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise OrderNotFoundException(order_id)

    if order.user_id != user.id:
        raise UnauthorizedOrderAccessException()

    order = session.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise OrderNotFoundException(order_id)

    order.products.clear()
    session.delete(order)
    session.commit()

    return {"message": "Order deleted Successfully. "}
