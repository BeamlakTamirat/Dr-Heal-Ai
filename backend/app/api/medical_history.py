
from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List, Optional
import logging

from app.database.connection import get_db
from app.models.database import User, MedicalHistory
from app.auth.security import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/medical-history", tags=["Medical History"])


class MedicalHistoryResponse(BaseModel):
    id: str
    symptoms: Optional[str]
    diagnosis: Optional[str]
    severity: Optional[str]
    agent_assessment: Optional[str]
    emergency_detected: Optional[str]
    date: str


@router.get("", response_model=List[MedicalHistoryResponse])
async def get_medical_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = 50,
    offset: int = 0
):
    
    try:
        history = db.query(MedicalHistory)\
            .filter(MedicalHistory.user_id == current_user.id)\
            .order_by(MedicalHistory.date.desc())\
            .limit(limit)\
            .offset(offset)\
            .all()
        
        return [
            MedicalHistoryResponse(
                id=str(entry.id),
                symptoms=entry.symptoms,
                diagnosis=entry.diagnosis,
                severity=entry.severity,
                agent_assessment=entry.agent_assessment,
                emergency_detected=entry.emergency_detected,
                date=entry.date.isoformat()
            )
            for entry in history
        ]
        
    except Exception as e:
        logger.error(f"Failed to get medical history: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve medical history"
        )


@router.get("/{history_id}", response_model=MedicalHistoryResponse)
async def get_medical_history_entry(
    history_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    
    try:
        entry = db.query(MedicalHistory)\
            .filter(
                MedicalHistory.id == history_id,
                MedicalHistory.user_id == current_user.id
            )\
            .first()
        
        if not entry:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Medical history entry not found"
            )
        
        return MedicalHistoryResponse(
            id=str(entry.id),
            symptoms=entry.symptoms,
            diagnosis=entry.diagnosis,
            severity=entry.severity,
            agent_assessment=entry.agent_assessment,
            emergency_detected=entry.emergency_detected,
            date=entry.date.isoformat()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get medical history entry: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve medical history entry"
        )


@router.delete("/{history_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_medical_history_entry(
    history_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    
    try:
        entry = db.query(MedicalHistory)\
            .filter(
                MedicalHistory.id == history_id,
                MedicalHistory.user_id == current_user.id
            )\
            .first()
        
        if not entry:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Medical history entry not found"
            )
        
        db.delete(entry)
        db.commit()
        
        logger.info(f"Medical history entry {history_id} deleted by user {current_user.email}")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete medical history entry: {e}", exc_info=True)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete medical history entry"
        )
