from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
import json
from rose_symptom_checker.schemas.diagnosis import (
    SymptomInput,
    DiagnosisResult,
    DiagnosisResponse,
    DiagnosisHistoryResponse
)
from rose_symptom_checker.schemas.base import BaseResponse
from rose_symptom_checker.db.models.user import User
from rose_symptom_checker.db.models.diagnosis import Diagnosis
from rose_symptom_checker.services.auth import get_current_user
from rose_symptom_checker.services.ml_predictor import predictor
from rose_symptom_checker.db.session import get_db
from rose_symptom_checker.core.exceptions import NotFoundException, BadRequestException

router = APIRouter(prefix="/diagnosis", tags=["Diagnosis"])


@router.post("/check", response_model=BaseResponse[DiagnosisResult])
async def check_symptoms(
    symptom_input: SymptomInput,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Check rose flower symptoms and predict disease
    """
    if not symptom_input.symptoms:
        raise BadRequestException("At least one symptom is required")
    
    # Predict disease
    disease, confidence = predictor.predict(symptom_input.symptoms)
    
    # Get recommendations
    recommendations = predictor.get_recommendations(disease)
    
    # Save to database
    diagnosis = Diagnosis(
        user_id=current_user.id,
        symptoms=json.dumps(symptom_input.symptoms),
        disease_predicted=disease,
        confidence_score=confidence,
        recommendations=json.dumps(recommendations)
    )
    
    db.add(diagnosis)
    db.commit()
    db.refresh(diagnosis)
    
    # Prepare response
    result = DiagnosisResult(
        disease=disease,
        confidence=confidence,
        symptoms_analyzed=symptom_input.symptoms,
        recommendations=recommendations
    )
    
    return BaseResponse.success_response(
        data=result,
        message="Diagnosis completed successfully"
    )


@router.get("/history", response_model=BaseResponse[DiagnosisHistoryResponse])
async def get_diagnosis_history(
    skip: int = 0,
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get user's diagnosis history
    """
    # Get total count
    total = db.query(Diagnosis).filter(Diagnosis.user_id == current_user.id).count()
    
    # Get paginated results
    diagnoses = (
        db.query(Diagnosis)
        .filter(Diagnosis.user_id == current_user.id)
        .order_by(Diagnosis.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    
    # Convert to response format
    items = [
        DiagnosisResponse(
            id=d.id,
            user_id=d.user_id,
            symptoms=json.loads(d.symptoms),
            disease_predicted=d.disease_predicted,
            confidence_score=d.confidence_score,
            recommendations=json.loads(d.recommendations),
            created_at=d.created_at
        )
        for d in diagnoses
    ]
    
    history = DiagnosisHistoryResponse(total=total, items=items)
    
    return BaseResponse.success_response(
        data=history,
        message="History retrieved successfully"
    )


@router.get("/history/{diagnosis_id}", response_model=BaseResponse[DiagnosisResponse])
async def get_diagnosis_by_id(
    diagnosis_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get specific diagnosis by ID
    """
    diagnosis = (
        db.query(Diagnosis)
        .filter(
            Diagnosis.id == diagnosis_id,
            Diagnosis.user_id == current_user.id
        )
        .first()
    )
    
    if not diagnosis:
        raise NotFoundException("Diagnosis not found")
    
    response = DiagnosisResponse(
        id=diagnosis.id,
        user_id=diagnosis.user_id,
        symptoms=json.loads(diagnosis.symptoms),
        disease_predicted=diagnosis.disease_predicted,
        confidence_score=diagnosis.confidence_score,
        recommendations=json.loads(diagnosis.recommendations),
        created_at=diagnosis.created_at
    )
    
    return BaseResponse.success_response(
        data=response,
        message="Diagnosis retrieved successfully"
    )


@router.get("/symptoms", response_model=BaseResponse[List[str]])
async def get_available_symptoms():
    """
    Get list of all available symptoms for diagnosis
    """
    symptoms = predictor.symptom_features if predictor.symptom_features else []
    
    return BaseResponse.success_response(
        data=symptoms,
        message="Available symptoms retrieved successfully"
    )