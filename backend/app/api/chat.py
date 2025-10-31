
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
import logging

from app.llm.rag_chain import get_rag_chain

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["AI Chat"])


class ChatRequest(BaseModel):
    query: str = Field(..., description="User's medical query", min_length=1)
    n_results: int = Field(5, description="Number of RAG results", ge=1, le=10)
    chat_type: Optional[str] = Field("symptoms", description="Query type: symptoms, disease, or general")


class RAGResult(BaseModel):
    name: str
    type: str
    similarity: float


class ChatResponse(BaseModel):
    query: str
    response: str
    rag_results: List[RAGResult]
    n_results: int


@router.post("/chat", response_model=ChatResponse)
async def chat_with_ai(request: ChatRequest):
    
    try:
        logger.info(f"Chat request: query='{request.query}', type={request.chat_type}")
        
        chain = get_rag_chain()
        
        if request.chat_type == "symptoms":
            result = chain.analyze_symptoms(
                query=request.query,
                n_results=request.n_results
            )
        elif request.chat_type == "disease":
            result = chain.get_disease_info(
                query=request.query,
                n_results=request.n_results
            )
        else: 
            result = chain.answer_question(
                query=request.query,
                n_results=request.n_results
            )
        
        rag_results = [
            RAGResult(
                name=r['metadata']['name'],
                type=r['metadata']['type'],
                similarity=round(r['similarity'], 3)
            )
            for r in result['rag_results']
        ]
        
        logger.info(f"Generated response (length: {len(result['response'])})")
        
        return ChatResponse(
            query=result['query'],
            response=result['response'],
            rag_results=rag_results,
            n_results=result['n_results']
        )
        
    except Exception as e:
        logger.error(f"Chat failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Chat failed: {str(e)}")


@router.post("/chat/symptoms")
async def analyze_symptoms(request: ChatRequest):
    
    request.chat_type = "symptoms"
    return await chat_with_ai(request)


@router.post("/chat/disease")
async def get_disease_info(request: ChatRequest):
    
    request.chat_type = "disease"
    return await chat_with_ai(request)