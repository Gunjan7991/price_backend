# Backend API

This is a backend API built with **FastAPI**, using **SQLite** as the database and **SQLModel** for ORM. The API includes authentication and supports CRUD operations.

## 🚀 Features

- **FastAPI**: High-performance web framework for APIs.
- **SQLite**: Lightweight database for storing application data.
- **SQLModel**: Combines Pydantic and SQLAlchemy for easy database interactions.
- **Authentication**: Secure login system using JWT tokens.
- **Modular Design**: Organized routers for different functionalities.

## 📦 Installation

1. **Clone the repository**  
   ```bash
   git clone <your-repo-url>
   cd <your-project-folder>
   ```

2. **Create a virtual environment**  
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the FastAPI server**  
   ```bash
   uvicorn main:app --reload
   ```

## 🛠️ Environment Variables

Create a `.env` file to store sensitive configurations:
```
SECRET_KEY=your_secret_key
ALGORITHM=HS256
DATABASE_URL=sqlite:///./database.db
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## 🔑 Authentication

The API uses JWT tokens for authentication:
1. **Login**: `/auth/login` (returns access token)
2. **Protected Routes**: Requires `Authorization: Bearer <token>` header.

## 📚 API Documentation

Once the server is running, visit:
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Redoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## 📌 Future Enhancements

- Role-based authentication
- Refresh token mechanism
- Dockerized deployment

