import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select
from typing import Annotated
import logging
import uuid

from .database import SessionDep, TokenData, User
from .config import SECRET_KEY,ALGORITHM,EXP_TIME
from .utils import verify_password, hash
# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

secret_key=SECRET_KEY
algorithm=ALGORITHM
exp_time = EXP_TIME

# Define exception
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid username or password",
    headers={"WWW-Authenticate": "Bearer"},
)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(
        minutes=exp_time
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt


def verify_access_token(token: str):
    try:
        payload = jwt.decode(
            token=token, key=secret_key, algorithms=algorithm
        )
        usr_id: str = payload.get("id")
        usr_name: str = payload.get("name")
        if usr_id is None:
            raise credentials_exceptions
        token_data = model.TokenData(id=str(usr_id), name=usr_name)
    except Exception as e:
        raise credentials_exceptions
    return token_data


async def get_current_user(session:SessionDep, token: Annotated[str, Depends(oauth2_scheme)])->User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        t_id: str = payload.get("id")
        t_name: str = payload.get("name")
        print(t_id)
        if t_id is None:
            raise credentials_exception
        token_data = TokenData(id=t_id, name=t_name)
    except InvalidTokenError:
        raise credentials_exception
    statement = select(User).where(User.id == uuid.UUID(t_id))
    user: User = session.exec(statement).first()
    if user is None:
        raise credentials_exception
    return user

def authenticate_and_generate_token(username, password, session):
    print(f"authenticate_and_generate_token- {username} , {password}")
    statement = select(User).where(User.email == str(username).upper())
    user:User = session.exec(statement).first()

    if not user or not verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials"
        )
    return create_access_token(data={"id": str(user.id), "name": str(user.name)})
