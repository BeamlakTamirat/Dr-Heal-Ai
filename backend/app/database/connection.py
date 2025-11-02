import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
from typing import Generator

from app.models.database import Base

logger = logging.getLogger(__name__)


class DatabaseManager:
    
    def __init__(self):
        self.database_url = os.getenv("DATABASE_URL")
        
        if not self.database_url:
            raise ValueError(
                "DATABASE_URL must be set in environment. "
                "Get it from Supabase: Settings -> Database -> Connection String (URI)"
            )
        
        if self.database_url.startswith("postgres://"):
            self.database_url = self.database_url.replace("postgres://", "postgresql://", 1)
        
        self.engine = create_engine(
            self.database_url,
            pool_pre_ping=True,
            pool_size=5,
            max_overflow=10
        )
        
        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine
        )
        
        logger.info("Database connection initialized")
    
    def create_tables(self):
        try:
            Base.metadata.create_all(bind=self.engine)
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Failed to create tables: {e}")
            raise
    
    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Database session error: {e}")
            raise
        finally:
            session.close()


_db_manager = None


def get_db_manager() -> DatabaseManager:
    global _db_manager
    
    if _db_manager is None:
        logger.info("Creating global database manager")
        _db_manager = DatabaseManager()
    
    return _db_manager


def get_db() -> Generator[Session, None, None]:
    db_manager = get_db_manager()
    with db_manager.get_session() as session:
        yield session