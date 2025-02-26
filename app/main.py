from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import init_db
import logging
from .routers import auth, user, getHeating,forgotPassword, order
from .createAdmin import createAdmin


init_db()
app = FastAPI()
origins = [ 
    "https://getb99.streamlit.app",    # Add production domain here
]

# Add CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    # allow_origins=origins,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(getHeating.router)
app.include_router(forgotPassword.router)
app.include_router(order.router)
@app.on_event("startup")
async def startup_event():
    if createAdmin():
        logging.info("ADMIN Created!!")
    else:
        logging.info("ADMIN already Exits!!")
