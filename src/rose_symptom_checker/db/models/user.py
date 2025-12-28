from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship
from rose_symptom_checker.db.base import Base, TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "users"
    
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    diagnoses = relationship("Diagnosis", back_populates="user", cascade="all, delete-orphan")

