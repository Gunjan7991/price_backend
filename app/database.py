from sqlmodel import SQLModel, create_engine, Field, Session
import uuid
from datetime import datetime
import logging
from fastapi import Depends
from typing import Annotated
from pydantic import EmailStr
from enum import Enum


class Role(str, Enum):
    USER = "user"
    ADMIN = "admin"

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

#Models
class Daily_Price(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    pricing: float
    created_at: datetime | None = Field(default_factory=datetime.utcnow)

class User(SQLModel,  table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    name: str = Field(nullable=False)
    email: str = Field(nullable=False, unique=True)
    password: str = Field(nullable=False)
    phone_number: str = Field(nullable=False)
    verified: bool = Field(default=False)
    role: Role = Field(default=Role.USER)
    reset_token: str | None = None  # Stores the reset code
    token_expiry: datetime | None = None  # Expiry time for reset token

class Order_Tracking(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    order_date: datetime | None 
    delivery_date: datetime | None
    bol: str
    delivery_price: float

class update_password(SQLModel):
    cur_password:str 
    new_password: str 

class reset_password(SQLModel):
    email:EmailStr
    reset_token:str 
    new_password: str 

class user_create(SQLModel):
    name: str
    email: EmailStr
    password: str 
    phone_number: str

class user_display(SQLModel):
    id: uuid.UUID 
    name: str 
    email: str 
    password: str
    phone_number: str 

"""
Token
"""
class Token(SQLModel):
    access_token: str
    token_type: str

class TokenData(SQLModel):
    id: str | None 
    name: str | None
    
#databse Config
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)



def init_db():
    try:
        SQLModel.metadata.create_all(engine)
        logging.info("DATABASE INITIALIZED SUCESSFULLY.")
    except Exception as e:
        logging.fatal(f"Failed to initialize database!{e}")


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]