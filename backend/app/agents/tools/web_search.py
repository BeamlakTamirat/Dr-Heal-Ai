
import logging
from typing import List, Dict, Any
from duckduckgo_search import DDGS

logger = logging.getLogger(__name__)


class MedicalWebSearchTool:

    def __init__(self):
        self.ddgs = DDGS()
        logger.info("Initialized MedicalWebSearchTool")
    
    def search(self, query: str, max_results: int = 3) -> List[Dict[str, Any]]:

        try:
            logger.info(f"Searching web for: '{query}' (max_results={max_results})")
            
            medical_query = f"{query} medical information site:nih.gov OR site:mayoclinic.org OR site:who.int"
            
            results = []
            search_results = self.ddgs.text(medical_query, max_results=max_results)
            
            for result in search_results:
                results.append({
                    'title': result.get('title', ''),
                    'snippet': result.get('body', ''),
                    'link': result.get('href', ''),
                    'source': self._extract_domain(result.get('href', ''))
                })
            
            logger.info(f"Found {len(results)} web results")
            return results
            
        except Exception as e:
            logger.error(f"Web search failed: {e}")
            return []
    
    def _extract_domain(self, url: str) -> str:
        try:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            return parsed.netloc
        except:
            return url
    
    def format_results(self, results: List[Dict[str, Any]]) -> str:
        if not results:
            return "No web search results found."
        
        formatted = "**Latest Medical Information from Web:**\n\n"
        for i, result in enumerate(results, 1):
            formatted += f"{i}. **{result['title']}**\n"
            formatted += f"   Source: {result['source']}\n"
            formatted += f"   {result['snippet']}\n"
            formatted += f"   Link: {result['link']}\n\n"
        
        return formatted
