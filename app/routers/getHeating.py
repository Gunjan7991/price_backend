from sqlmodel import select, desc
from fastapi import APIRouter, HTTPException, status, Depends
from typing import Annotated
import logging
from datetime import datetime

from ..database import SessionDep, Daily_Price, Role, User
from ..utils import get_heating_oil
from ..oauth import get_current_user

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
router = APIRouter(prefix="/api/v1/oil", tags=["OIL"])

@router.post('')
def add_pricing(session: SessionDep,  current_user: Annotated[User, Depends(get_current_user)]):
    user: User = current_user
    if user.role != Role.ADMIN:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    price = get_heating_oil()
    daily_price: Daily_Price = Daily_Price(pricing= price)
    statement = select(Daily_Price).order_by(desc(Daily_Price.created_at)).limit(1)
    latest_pricing:Daily_Price = session.exec(statement).first()
    if latest_pricing:
        current_date = datetime.utcnow().date()
        latest_date = latest_pricing.created_at.date()  # Extract date from datetime
        if latest_date == current_date:
            logging.info("Daily Price already updated!!")
            raise HTTPException(
                status_code=status.HTTP_208_ALREADY_REPORTED,
                detail="Daily price already updated!!"
            )

    try:
        session.add(daily_price)
        session.commit()
        session.refresh(daily_price)
    except Exception as e:
        session.rollback()  # Rollback transaction on failure
        logging.error(f"Purchase update failed: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Request not completed!")
    return daily_price

@router.get('')
def get_latest(session: SessionDep):
    statement = select(Daily_Price).order_by(desc(Daily_Price.created_at)).limit(1)
    latest_pricing = session.exec(statement).first()
    if not latest_pricing:
        return {"message": "No price data available"}
    
    return latest_pricing

@router.get('/all')
def get_latest(session: SessionDep,  current_user: Annotated[User, Depends(get_current_user)]):
    statement = select(Daily_Price).limit(7)
    pricing = session.exec(statement).all()
    return pricing
