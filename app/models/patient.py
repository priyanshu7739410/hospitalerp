from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, Boolean, DateTime
from app.models.base import Base

# Step 1: Define the Patient Model
# We inherit from Base so SQLAlchemy knows this class represents a database table.
class Patient(Base):
    # __tablename__ is the exact name the table will have inside PostgreSQL.
    __tablename__ = "patients"

    # Step 2: Define Columns
    # Column(Integer, primary_key=True, index=True): Auto-incrementing ID. We index it so lookups by ID are blazing fast.
    id = Column(Integer, primary_key=True, index=True)
    
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    
    # unique=True: Ensures no two patients can register with the same email. PostgreSQL enforces this at the hardware level.
    # index=True: We will often search for patients by email when logging in or checking records, so we index it.
    email = Column(String(100), unique=True, index=True, nullable=False)
    phone = Column(String(20), nullable=True)
    
    date_of_birth = Column(Date, nullable=False)
    gender = Column(String(10), nullable=False)
    blood_group = Column(String(5), nullable=True)
    
    is_active = Column(Boolean, default=True)
    
    # default=datetime.utcnow: Automatically records the exact timestamp when a row is inserted.
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # __repr__ makes debugging in Python much cleaner when printing patient objects.
    def __repr__(self):
        return f"<Patient {self.first_name} {self.last_name} (ID: {self.id})>"
