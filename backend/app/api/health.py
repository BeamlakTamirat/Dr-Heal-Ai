from fastapi import APIRouter, HTTPException
from datetime import datetime
import asyncio
from app.utils.metrics import get_metrics

router = APIRouter(prefix="/api", tags=["Health"])

@router.get("/health")
async def health_check():
    return {"status": "healthy"}

@router.get("/health/detailed")
async def detailed_health_check():
    try:
        metrics = get_metrics()
        
        db_status = await check_database_health()
        vector_status = await check_vector_store_health()
        llm_status = await check_llm_health()
        
        overall_status = "healthy" if all([db_status, vector_status, llm_status]) else "degraded"
        
        return {
            "status": overall_status,
            "timestamp": datetime.utcnow().isoformat(),
            "components": {
                "database": "healthy" if db_status else "unhealthy",
                "vector_store": "healthy" if vector_status else "unhealthy",
                "llm_service": "healthy" if llm_status else "unhealthy"
            },
            "metrics": metrics.get_stats()
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }

async def check_database_health() -> bool:
    try:
        from app.database.connection import get_db_manager
        db_manager = get_db_manager()
        with db_manager.get_session() as session:
            session.execute("SELECT 1")
        return True
    except:
        return False

async def check_vector_store_health() -> bool:
    try:
        from app.rag.vectorstore import get_vector_store
        vector_store = get_vector_store()
        count = vector_store.get_document_count()
        return count > 0
    except:
        return False

async def check_llm_health() -> bool:
    try:
        from app.llm.gemini import get_gemini_llm
        llm = get_gemini_llm()
        response = llm.generate("test")
        return len(response) > 0
    except:
        return False
