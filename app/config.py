import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


# JWT Authentication Configuration

SECRET_KEY = os.getenv("SECRET_KEY", "your_default_secret")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
EXP_TIME = int(os.getenv("EXP_TIME", 60))  # Token expiration time in minutes
EMAIL = os.getenv("EMAIL", "USER@EMAIL.COM")
PASSWORD = os.getenv("PASSWORD", "JDIjd90sdJSA")
