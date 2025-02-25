from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select, Session
from datetime import datetime, timedelta
import secrets
from typing import Annotated
from ..database import get_session, User, reset_password
from ..sendEmail import send_email  # Assume you have an email function
from ..utils import hash
from ..oauth import get_current_user

router = APIRouter(tags=["RESET_PASSWORD"])

@router.post("/forgot-password")
def forgot_password(email: str, session: Session = Depends(get_session)):
    statement = select(User).where(User.email == email.upper())
    user = session.exec(statement).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Generate reset token
    reset_token = str(secrets.token_hex(16))
    expiry_time = datetime.utcnow() + timedelta(minutes=15)  # Token valid for 15 minutes

    # Save to database
    user.reset_token = reset_token
    user.token_expiry = expiry_time
    session.add(user)
    session.commit()

    send_email(email, "Password Reset Code", f"Your password reset code: {reset_token}")

    return {"message": "Password reset code sent. Please check your email."}


@router.put("/reset")
def reset_password(reset: reset_password, session: Session = Depends(get_session)):
    user:User = session.exec(select(User).where(User.email == reset.email.upper())).first()
    if user.reset_token != reset.reset_token:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,  detail="Incorrect Credentials!")
    user.password = hash(reset.new_password)
    try:
        session.add(user)
        session.commit()
        session.refresh(user)
    except e as Exception:
        session.rollback()  # Rollback transaction on failure
        logging.error(f"Purchase update failed: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Request not completed!")
    raise HTTPException(status_code=status.HTTP_201_CREATED,  detail="Password Change Sucessfull")

