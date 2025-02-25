import uuid
from sqlmodel import Session
from .database import engine, User, Role  # Import your database connection
from .utils import hash  # Ensure passwords are hashed


def createAdmin():
    session = Session(engine)
    existing_admin = session.query(User).filter(User.role == Role.ADMIN).first()
    if existing_admin:
        print("Admin already exists.")
        session.close()
        return False
    else:
        # Create first admin
        admin_user = User(
            id=uuid.uuid4(),
            name="Super Admin",
            email="ALGU.BUSINESS@GMAIL.COM",
            password=hash("StrongAdminPassword123!!"),  # Replace with a strong password
            phone_number="1234567890",
            verified=True,
            role=Role.ADMIN
        )

        session.add(admin_user)
        session.commit()
        print("First admin created successfully.")
        session.close()
        return True
    
