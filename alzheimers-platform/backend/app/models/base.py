# backend/app/models/base.py
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

# backend/app/models/user.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON
from .base import Base
import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    role = Column(String)  # patient, doctor, nurse, admin
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    preferred_language = Column(String, default="en")
    mfa_secret = Column(String, nullable=True)

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    mrn = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    date_of_birth = Column(DateTime)
    sex = Column(String)
    contact_phone = Column(String)
    emergency_contact = Column(String)
    preferred_language = Column(String, default="en")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

# Additional models for Intake, Symptoms, Tests, etc.