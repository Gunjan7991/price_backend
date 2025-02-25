from fastapi import APIRouter, Depends, Request, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from typing import Annotated
from ..database import SessionDep, User, Token
from ..oauth import authenticate_and_generate_token


router = APIRouter(prefix="", tags=["Authentication"])

# Define exception
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid username or password",
    headers={"WWW-Authenticate": "Bearer"},
)
@router.post("/login", status_code=status.HTTP_202_ACCEPTED, response_model=Token)
async def login(session:SessionDep, login_cred: Annotated[OAuth2PasswordRequestForm, Depends()]):
    try:
        print(f"login- {login_cred.username} || {login_cred.password}")
        username = login_cred.username
        print(f"username- {username}")
        password =  login_cred.password
        print(f"password-  {password}")
        token = authenticate_and_generate_token(username, password, session)
        return Token(access_token=token, token_type="Bearer")
    except Exception as e:
        print(e)
        raise  credentials_exception
