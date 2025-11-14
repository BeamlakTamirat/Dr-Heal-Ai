import os
from typing import Optional
import logging
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GeminiLLM:
    def __init__(
        self,
        model_name:str = "gemini-2.5-flash",
        temperature: float = 0.7,
        max_tokens: Optional[int] = 2048
    ):
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY not found in environment variables. "
                "Please set it in .env file."
            )
        
        logger.info(f"Initializing Gemini model: {model_name}")
        
        try:
            
            self.llm = ChatGoogleGenerativeAI(
                model=model_name,
                google_api_key=api_key,
                temperature=temperature,
                max_output_tokens=max_tokens,
                convert_system_message_to_human=True  
            )
            
            logger.info("Gemini LLM initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Gemini: {e}")
            raise
    
    def generate(self, prompt: str) -> str:
        try:
            from app.utils.resilience import with_timeout, retry_with_backoff
            import asyncio
            
            async def _generate():
                response = self.llm.invoke(prompt)
                return response.content
            
            async def _generate_with_timeout():
                return await with_timeout(_generate(), 30.0)
            
            return asyncio.run(retry_with_backoff(_generate_with_timeout))
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return "I'm experiencing technical difficulties. Please try again or consult a healthcare provider."
    
    def get_model(self):
        return self.llm


_gemini_llm = None


def get_gemini_llm() -> GeminiLLM:
    global _gemini_llm
    
    if _gemini_llm is None:
        logger.info("Creating global Gemini LLM instance")
        _gemini_llm = GeminiLLM()
    
    return _gemini_llm
