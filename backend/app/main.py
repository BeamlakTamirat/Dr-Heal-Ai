from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.api.rag import router as rag_router
from app.api.chat import router as chat_router
from app.api.auth import router as auth_router
from app.api.conversations import router as conversations_router
from app.api.medical_history import router as medical_history_router
from app.database.connection import get_db_manager
from app.middleware import RateLimitMiddleware

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Dr.Heal AI API",
    description="AI-powered medical assistant with multi-agent system",
    version="2.0.0"
)

app.add_middleware(RateLimitMiddleware, calls=100, period=60)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(conversations_router)
app.include_router(medical_history_router)
app.include_router(rag_router)
app.include_router(chat_router)


@app.on_event("startup")
async def startup_event():
    try:
        logger.info("Initializing database...")
        db_manager = get_db_manager()
        db_manager.create_tables()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")


@app.get("/")
async def root():
    return {
        "message": "Dr.Heal AI API is running",
        "status": "healthy",
        "version": "2.0.0",
        "features": [
            "Multi-agent medical assistant",
            "User authentication",
            "Conversation history",
            "Medical history tracking",
            "Rate limiting (100 req/min)"
        ]
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
