import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.llm.gemini import get_gemini_llm
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_gemini_connection():
    logger.info("="*60)
    logger.info("GEMINI API CONNECTION TEST")
    logger.info("="*60)
    
    try:
        logger.info("\nStep 1: Initializing Gemini LLM...")
        llm = get_gemini_llm()
        logger.info("✅ Gemini initialized successfully")
        
        logger.info("\nStep 2: Testing simple query...")
        prompt = "What is fever? Answer in one sentence."
        
        logger.info(f"Prompt: {prompt}")
        response = llm.generate(prompt)
        
        logger.info(f"\nResponse: {response}")
        logger.info("✅ Query successful")
        
        logger.info("\nStep 3: Testing medical query...")
        prompt = "What are the common symptoms of flu?"
        
        logger.info(f"Prompt: {prompt}")
        response = llm.generate(prompt)
        
        logger.info(f"\nResponse: {response}")
        logger.info("✅ Medical query successful")
        
        logger.info("\n" + "="*60)
        logger.info("✅ ALL TESTS PASSED!")
        logger.info("="*60)
        logger.info("\nGemini API is working correctly.")
        logger.info("Ready to integrate with RAG system.")
        
    except Exception as e:
        logger.error(f"\n❌ TEST FAILED: {e}", exc_info=True)
        logger.error("\nPlease check:")
        logger.error("1. GEMINI_API_KEY is set in .env file")
        logger.error("2. API key is valid")
        logger.error("3. Internet connection is working")
        sys.exit(1)


if __name__ == "__main__":
    test_gemini_connection()