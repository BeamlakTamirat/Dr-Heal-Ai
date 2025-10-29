from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
import logging

from app.rag.medical_rag import get_medical_rag

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["RAG Search"])


class SearchRequest(BaseModel):

    query: str = Field(..., description="Search query", min_length=1)
    n_results: int = Field(5, description="Number of results", ge=1, le=20)
    filter_type: Optional[str] = Field(None, description="Filter by type: 'symptom' or 'disease'")


class SearchResult(BaseModel):
    
    name: str
    type: str
    id: str
    similarity: float
    text: str


class SearchResponse(BaseModel):
    
    query: str
    results: List[SearchResult]
    count: int


@router.post("/search", response_model=SearchResponse)
async def search_medical_knowledge(request: SearchRequest):
    
    try:
        logger.info(f"Search request: query='{request.query}', n_results={request.n_results}, filter={request.filter_type}")
        
        rag = get_medical_rag()
        
        results = rag.search(
            query=request.query,
            n_results=request.n_results,
            filter_type=request.filter_type
        )
        
        formatted_results = [
            SearchResult(
                name=r['metadata']['name'],
                type=r['metadata']['type'],
                id=r['metadata']['id'],
                similarity=round(r['similarity'], 3),
                text=r['text']
            )
            for r in results
        ]
        
        logger.info(f"Found {len(formatted_results)} results")
        
        return SearchResponse(
            query=request.query,
            results=formatted_results,
            count=len(formatted_results)
        )
        
    except Exception as e:
        logger.error(f"Search failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@router.get("/search/stats")
async def get_search_stats():
    
    try:
        rag = get_medical_rag()
        
        return {
            "total_documents": rag.vector_store.get_document_count(),
            "embedding_dimension": rag.embedding_model.get_dimension(),
            "storage_path": rag.vector_store.persist_directory
        }
        
    except Exception as e:
        logger.error(f"Failed to get stats: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))