from sqlalchemy import Column, String, Integer, ForeignKey, Float, Text
from sqlalchemy.orm import relationship
from rose_symptom_checker.db.base import Base, TimestampMixin


class Diagnosis(Base, TimestampMixin):
    __tablename__ = "diagnoses"
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    symptoms = Column(Text, nullable=False)  # JSON string
    disease_predicted = Column(String, nullable=False)
    confidence_score = Column(Float, nullable=False)
    recommendations = Column(Text)  # JSON string
    
    # Relationships
    user = relationship("User", back_populates="diagnoses")