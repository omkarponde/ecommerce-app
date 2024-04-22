from datetime import datetime
from fastapi import APIRouter, status, Depends, Header
from app.models import Order, Product, OrderProductAssociation
from app.dependencies import get_db, can_buy_product, is_user_authorized
from fastapi.exceptions import HTTPException
from typing import List
from app.schemas import CreateOrderModel
from collections import defaultdict
import stripe
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.config import settings
from app.exceptions import UserNotFoundException, ProductNotFoundException, InvalidPriceValueException, \
    UnauthorizedProductAccessException, PermissionDeniedException, UnauthorizedProductAccessException
from app.db import Session

stripe.api_key = settings.STRIPE_KEY

order_router = APIRouter(
    prefix=''
)


@order_router.get('/ping/', status_code=status.HTTP_200_OK)
def ping_orders(user: dict = Depends(is_user_authorized)):
    if user['role'] == "seller":
        raise PermissionDeniedException()

    return {
        "message": "You are authorized to see the orders"
    }


@order_router.get('/my-orders/', status_code=status.HTTP_200_OK)
def get_my_orders(
        user: dict = Depends(can_buy_product),
        session: Session = Depends(get_db)
):
    orders = session.query(Order).filter(Order.user_id == user['user_id']).all()
    return orders


@order_router.get('/{order_id}', status_code=status.HTTP_200_OK)
def get_order_by_id(
        order_id: int,
        user: dict = Depends(is_user_authorized),
        session: Session = Depends(get_db)
):
    if user['role'] == 'seller':
        PermissionDeniedException()
    order = session.query(Order).filter(Order.id == order_id).first()
    if user['role'] == 'buyer' and order.user_id != user['user_id']:
        PermissionDeniedException()

    return order


@order_router.get('/all-orders/', status_code=status.HTTP_200_OK)
def get_all_orders(
        user: dict = Depends(is_user_authorized),
        session: Session = Depends(get_db)
):
    if user['role'] != 'admin':
        PermissionDeniedException()
    orders = session.query(Order).all()
    return orders


@order_router.post('/', status_code=status.HTTP_200_OK)
def create_order_with_lock(
        payload: CreateOrderModel,
        user: dict = Depends(can_buy_product),
        session: Session = Depends(get_db)
):
    total_cost = 0
    product_list = payload.order_data
    resultant_products = sorted(product_list, key=lambda x: x[0])
    product_ids = [product_data[0] for product_data in resultant_products]

    with session.begin():
        # Apply pessimistic lock while selecting products
        products = session.execute(
            select(Product).filter(Product.id.in_(product_ids)).with_for_update()
        ).scalars().all()

        if len(products) < len(product_ids):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="One or more products not found."
            )

        for index, product in enumerate(products):
            if resultant_products[index][1] > product.quantity_available:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Insufficient quantity available."
                )
            total_cost += (product.price * resultant_products[index][1])
            product.quantity_available -= resultant_products[index][1]

        new_order = Order(
            user_id=user['user_id'],
            price=total_cost,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            status='Processing'
        )

        session.add(new_order)
    #     TODO: Here payment integration has to be done where if the payment is successfull,/
    #      then only the transaction is completed

    return {"message": "Order created successfully.", "total_cost": total_cost}


# below endpoints are yet to be implemented, from them to be a part of the code certain changes has to be made.
@order_router.post("/process-payment/")
async def process_payment():
    try:
        amount = 10000
        payment_intent = stripe.PaymentIntent.create(
            amount=amount,
            currency="inr"
        )
        return payment_intent.client_secret
    except stripe.error.StripeError as e:
        return HTTPException(status_code=400, detail=str(e))


@order_router.post("/webhook")
async def stripe_webhook(payload: dict):
    try:
        # Retrieve the event
        event = stripe.Event.construct_from(
            payload, stripe.api_key, stripe_version=None
        )

        # Handle the event
        if event.type == "payment_intent.succeeded":
            payment_intent = event.data.object
            # Handle successful payment

        # Acknowledge receipt of the event
        return {"received": True}
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))
