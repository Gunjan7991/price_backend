from sqlmodel import select
from fastapi import APIRouter, HTTPException, status, Depends, Request
from typing import Annotated
import logging


from ..database import SessionDep, Order, Order_Tracking, User, Update_Order
from ..oauth import get_current_user

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
router = APIRouter(prefix="/api/v1/order", tags=["ORDER"])

@router.post('')
def create_order(new_order: Order,  session:SessionDep,  current_user: Annotated[User, Depends(get_current_user)]):
    order: Order_Tracking = Order_Tracking(**new_order.model_dump())
    order.user_id = current_user.id
    try:
        session.add(order)
        session.commit()
        session.refresh(oder)
    except Exception as e:
        session.rollback()  # Rollback transaction on failure
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Request not completed!")
    return order

@router.get('')
def get_order(session:SessionDep ,current_user: Annotated[User, Depends(get_current_user)], skip:int = 0):
    orders:[Order_Tracking] = session.exec(select(Order_Tracking).where(Order_Tracking.user_id == current_user.id).limit(10).offset(skip*10)).all()
    return orders

@router.put('')
def update_order(update_order: Update_Order,  session:SessionDep,  current_user: Annotated[User, Depends(get_current_user)]):
    order: Order_Tracking = session.exec(select(Order_Tracking).where(Order_Tracking.id == update_order.id)).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="No Order with that order id")
    if update_order.bol:
        order.bol = update_order.bol
    if update_order.delivery_date:
        order.delivery_date = update_order.delivery_date
    if update_order.order_date:
        order.order_date = update_order.order_date
    if update_order.delivery_price:
        order.delivery_price = update_order.delivery_price
    try:
        session.add(order)
        session.commit()
        session.refresh(oder)
    except Exception as e:
        session.rollback()  # Rollback transaction on failure
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Request not completed!")
    return order