from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class SymptomInput(BaseModel):
    symptoms: List[str] = Field(
        ...,
        description="List of observed symptoms",
        example=["dark_spots_on_leaves", "yellowing_leaves", "leaf_drop"]
    )


class DiagnosisResult(BaseModel):
    disease: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    symptoms_analyzed: List[str]
    recommendations: List[str]


class DiagnosisCreate(BaseModel):
    symptoms: List[str]
    disease_predicted: str
    confidence_score: float
    recommendations: List[str]


class DiagnosisResponse(BaseModel):
    id: int
    user_id: int
    symptoms: List[str]
    disease_predicted: str
    confidence_score: float
    recommendations: List[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


class DiagnosisHistoryResponse(BaseModel):
    total: int
    items: List[DiagnosisResponse]