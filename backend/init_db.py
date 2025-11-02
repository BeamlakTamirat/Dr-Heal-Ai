import os
import sys
import logging
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(__file__))

from app.database.connection import get_db_manager

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def init_database():
    try:
        load_dotenv()
        
        logger.info("Starting database initialization...")
        
        required_vars = ["SUPABASE_URL", "SUPABASE_KEY"]
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
            logger.error("Please set them in your .env file")
            return False
        
        database_url = os.getenv("SUPABASE_URL")
        logger.debug(f"Using SUPABASE_URL: {database_url}")
        
        db_manager = get_db_manager()
        db_manager.create_tables()
        
        logger.info("✅ Database initialized successfully!")
        logger.info("Tables created:")
        logger.info("  - users")
        logger.info("  - conversations")
        logger.info("  - messages")
        logger.info("  - medical_history")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}", exc_info=True)
        return False


if __name__ == "__main__":
    success = init_database()
    sys.exit(0 if success else 1)