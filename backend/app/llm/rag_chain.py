import logging
from typing import Dict, List
from langchain.chains import LLMChain
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from app.rag.medical_rag import get_medical_rag
from app.llm.gemini import get_gemini_llm
from app.llm.prompts import (
    get_symptom_analysis_prompt,
    get_disease_info_prompt,
    get_general_medical_prompt
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MedicalRAGChain:
    def __init__(self):
        logger.info("Initializing Medical RAG Chain")
        
        self.rag = get_medical_rag()
        self.llm = get_gemini_llm()
        
        self.symptom_prompt = get_symptom_analysis_prompt()
        self.disease_prompt = get_disease_info_prompt()
        self.general_prompt = get_general_medical_prompt()
        
        logger.info("Medical RAG Chain initialized successfully")
    
    
    def _format_context(self, rag_results: List[Dict]) -> str:
        if not rag_results:
            return "No relevant medical information found in the knowledge base."
        
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
    
    
    def analyze_symptoms(
        self,
        query: str,
        n_results: int = 5
    ) -> Dict[str, any]:
        try:
            logger.info(f"Analyzing symptoms: '{query}'")
            
            logger.info("Step 1: Retrieving medical knowledge...")
            rag_results = self.rag.search(query, n_results=n_results)
            
            logger.info(f"Retrieved {len(rag_results)} results")
            
            logger.info("Step 2: Formatting context...")
            context = self._format_context(rag_results)
            
            logger.info("Step 3: Generating AI response...")
            prompt_text = self.symptom_prompt.format(
                context=context,
                query=query
            )
            
            response = self.llm.generate(prompt_text)
            
            logger.info(f"Generated response (length: {len(response)})")
            
            return {
                "query": query,
                "response": response,
                "context": context,
                "rag_results": rag_results,
                "n_results": len(rag_results)
            }
            
        except Exception as e:
            logger.error(f"Symptom analysis failed: {e}", exc_info=True)
            raise
    
    
    def get_disease_info(
        self,
        query: str,
        n_results: int = 3
    ) -> Dict[str, any]:
        try:
            logger.info(f"Getting disease info: '{query}'")
            
            rag_results = self.rag.search_diseases(query, n_results=n_results)
            
            context = self._format_context(rag_results)
            
            prompt_text = self.disease_prompt.format(
                context=context,
                query=query
            )
            
            response = self.llm.generate(prompt_text)
            
            return {
                "query": query,
                "response": response,
                "context": context,
                "rag_results": rag_results,
                "n_results": len(rag_results)
            }
            
        except Exception as e:
            logger.error(f"Disease info retrieval failed: {e}", exc_info=True)
            raise
    
    
    def answer_question(
        self,
        query: str,
        n_results: int = 5
    ) -> Dict[str, any]:
        try:
            logger.info(f"Answering question: '{query}'")
            
            rag_results = self.rag.search(query, n_results=n_results)
            
            context = self._format_context(rag_results)
            
            prompt_text = self.general_prompt.format(
                context=context,
                query=query
            )
            
            response = self.llm.generate(prompt_text)
            
            return {
                "query": query,
                "response": response,
                "context": context,
                "rag_results": rag_results,
                "n_results": len(rag_results)
            }
            
        except Exception as e:
            logger.error(f"Question answering failed: {e}", exc_info=True)
            raise


_rag_chain = None


def get_rag_chain() -> MedicalRAGChain:
    global _rag_chain
    
    if _rag_chain is None:
        logger.info("Creating global RAG chain instance")
        _rag_chain = MedicalRAGChain()
    
    return _rag_chain