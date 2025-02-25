from sqlmodel import select
from fastapi import APIRouter, HTTPException, status, Depends, Request
from typing import Annotated
import logging
from pydantic import EmailStr

from ..database import SessionDep,User, update_password, user_create, user_display, reset_password
from ..utils import hash, verify_password
from ..oauth import get_current_user

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
router = APIRouter(prefix="/api/v1/user", tags=["USER"])

@router.post("",response_model=user_display, status_code=status.HTTP_201_CREATED)
def create_user(new_user: user_create, session: SessionDep):
    new_user.email = str(new_user.email).upper()
    user:User = User(**new_user.model_dump())
    statement = select(User).where(User.email == user.email)
    user_exists: User = session.exec(statement).first()
    if user_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Email Already Exists!!")
    if user.phone_number:
        user.phone_number = user.phone_number.replace("-","").replace("(", "").replace(")","").replace(" ","")
    
    statement = select(User).where(User.phone_number == user.phone_number)
    user_exists: User = session.exec(statement).first()
    if user_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Phone Already Exists!!")
    user.password = hash(user.password)
    try:
        session.add(user)
        session.commit()
        session.refresh(user)
    except Exception as e:
        session.rollback()  # Rollback transaction on failure
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Request not completed!")
    return user

@router.get("",  response_model=user_display,  status_code=status.HTTP_200_OK)
def get_user(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user

@router.get("/all", status_code=status.HTTP_200_OK)
def get_user(session: SessionDep):
    statement = select(User)
    users = session.exec(statement).all()
    return users

@router.put("/update/password")
def update_password(update: update_password, session:SessionDep,  current_user:Annotated[User, Depends(get_current_user)]):
    if not verify_password(update.current_password, current_user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password didn't match!")
    current_user.password = hash(update.new_password)
    try:
        session.add(current_user)
        session.commit()
        session.refresh(current_user)
    except e as Exception:
        session.rollback()  # Rollback transaction on failure
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Request not completed!")
    raise HTTPException(status_code=status.HTTP_201_CREATED,  detail="Password Change Sucessfull")

@router.put("/update/role")
def update_role(email: EmailStr, session:SessionDep,  current_user:Annotated[User, Depends(get_current_user)]):
    if current_user.role != Role.ADMIN:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized!")
    client: User = session.exec(select(User).where(User.email == email)).first()
    client.role = Role.ADMIN
    try:
        session.add(client)
        session.commit()
        session.refresh(client)
    except e as Exception:
        session.rollback()  # Rollback transaction on failure
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Request not completed!")
    raise HTTPException(status_code=status.HTTP_201_CREATED,  detail="ROLE Change Sucessfull")