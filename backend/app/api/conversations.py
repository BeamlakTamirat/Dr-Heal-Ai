
from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import logging

from app.database.connection import get_db
from app.models.database import User, Conversation, Message, MedicalHistory
from app.auth.security import get_current_user
from app.agents.workflow import get_workflow

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/conversations", tags=["Conversations"])


class MessageResponse(BaseModel):
    id: str
    role: str
    content: str
    agent_used: Optional[str]
    timestamp: str


class ConversationResponse(BaseModel):
    id: str
    title: str
    created_at: str
    updated_at: str
    message_count: int


class ConversationDetailResponse(BaseModel):
    id: str
    title: str
    created_at: str
    updated_at: str
    messages: List[MessageResponse]


class ChatRequest(BaseModel):
    conversation_id: Optional[str] = None
    query: str = Field(..., min_length=1, max_length=1000)


class ChatResponse(BaseModel):
    conversation_id: str
    message_id: str
    response: str
    agent_used: str


@router.get("", response_model=List[ConversationResponse])
async def get_conversations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = 50,
    offset: int = 0
):
    
    try:
        conversations = db.query(Conversation)\
            .filter(Conversation.user_id == current_user.id)\
            .order_by(Conversation.updated_at.desc())\
            .limit(limit)\
            .offset(offset)\
            .all()
        
        return [
            ConversationResponse(
                id=str(conv.id),
                title=conv.title or "New Conversation",
                created_at=conv.created_at.isoformat(),
                updated_at=conv.updated_at.isoformat(),
                message_count=len(conv.messages)
            )
            for conv in conversations
        ]
        
    except Exception as e:
        logger.error(f"Failed to get conversations: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve conversations"
        )


@router.get("/{conversation_id}", response_model=ConversationDetailResponse)
async def get_conversation(
    conversation_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    
    try:
        conversation = db.query(Conversation)\
            .filter(
                Conversation.id == conversation_id,
                Conversation.user_id == current_user.id
            )\
            .first()
        
        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )
        
        messages = db.query(Message)\
            .filter(Message.conversation_id == conversation_id)\
            .order_by(Message.timestamp.asc())\
            .all()
        
        return ConversationDetailResponse(
            id=str(conversation.id),
            title=conversation.title or "New Conversation",
            created_at=conversation.created_at.isoformat(),
            updated_at=conversation.updated_at.isoformat(),
            messages=[
                MessageResponse(
                    id=str(msg.id),
                    role=msg.role,
                    content=msg.content,
                    agent_used=msg.agent_used,
                    timestamp=msg.timestamp.isoformat()
                )
                for msg in messages
            ]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get conversation: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve conversation"
        )


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    
    try:
        if request.conversation_id:
            conversation = db.query(Conversation)\
                .filter(
                    Conversation.id == request.conversation_id,
                    Conversation.user_id == current_user.id
                )\
                .first()
            
            if not conversation:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Conversation not found"
                )
        else:
            conversation = Conversation(
                user_id=current_user.id,
                title=request.query[:50] 
            )
            db.add(conversation)
            db.commit()
            db.refresh(conversation)
        
        user_message = Message(
            conversation_id=conversation.id,
            role="user",
            content=request.query
        )
        db.add(user_message)
        db.commit()
        
        workflow = get_workflow()
        result = workflow.process(request.query)
        
        agent_used = None
        if result.get('agent_outputs'):
            outputs = result['agent_outputs']
            if outputs.get('symptom_analysis'):
                agent_used = "SymptomAnalyzer"
            elif outputs.get('disease_info'):
                agent_used = "DiseaseExpert"
            elif outputs.get('treatment_advice'):
                agent_used = "TreatmentAdvisor"
            elif outputs.get('emergency_triage'):
                agent_used = "EmergencyTriage"
        
        response_text = result.get('final_response', 'No response generated')
        
        ai_message = Message(
            conversation_id=conversation.id,
            role="assistant",
            content=response_text,
            agent_used=agent_used
        )
        db.add(ai_message)
        
        conversation.updated_at = datetime.utcnow()
        
        if agent_used == "EmergencyTriage":
            medical_entry = MedicalHistory(
                user_id=current_user.id,
                symptoms=request.query,
                agent_assessment=response_text,
                emergency_detected="true",
                severity="severe"
            )
            db.add(medical_entry)
        
        db.commit()
        db.refresh(ai_message)
        
        logger.info(f"Chat processed for user {current_user.email}, agent: {agent_used}")
        
        return ChatResponse(
            conversation_id=str(conversation.id),
            message_id=str(ai_message.id),
            response=response_text,
            agent_used=agent_used or "Unknown"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Chat failed: {e}", exc_info=True)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chat processing failed: {str(e)}"
        )


@router.delete("/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_conversation(
    conversation_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a conversation and all its messages.
    """
    try:
        conversation = db.query(Conversation)\
            .filter(
                Conversation.id == conversation_id,
                Conversation.user_id == current_user.id
            )\
            .first()
        
        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )
        
        db.delete(conversation)
        db.commit()
        
        logger.info(f"Conversation {conversation_id} deleted by user {current_user.email}")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete conversation: {e}", exc_info=True)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete conversation"
        )
