from typing import Dict, Any, List
from abc import ABC, abstractmethod
import logging

from app.rag.medical_rag import get_medical_rag
from app.llm.gemini import get_gemini_llm
from app.agents.tools.web_search import MedicalWebSearchTool

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    def __init__(self, name: str, role: str):
        
        self.name = name
        self.role = role
        self.rag = get_medical_rag()
        self.llm = get_gemini_llm()
        self.web_search = MedicalWebSearchTool()
        
        logger.info(f"Initialized {name} agent")
    
    
    @abstractmethod
    def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        pass
    
    
    def retrieve_knowledge(
        self,
        query: str,
        n_results: int = 5,
        filter_type: str = None
    ) -> List[Dict]:
        return self.rag.search(
            query=query,
            n_results=n_results,
            filter_type=filter_type
        )
    
    
    def generate_response(self, prompt: str) -> str:
        return self.llm.generate(prompt)
    
    
    def format_context(self, rag_results: List[Dict]) -> str:
        if not rag_results:
            return "No relevant information found."
        
        context_parts = []
        for i, result in enumerate(rag_results, 1):
            name = result['metadata']['name']
            doc_type = result['metadata']['type']
            similarity = result['similarity']
            text = result['text']
            
            context_parts.append(
                f"{i}. {name} ({doc_type}, {similarity*100:.0f}% match)\n{text}\n"
            )
        
        return "\n".join(context_parts)