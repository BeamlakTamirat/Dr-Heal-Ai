
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
            from app.utils.resilience import with_timeout
            import asyncio
            
            logger.info(f"Searching web for: '{query}'")
            
            async def _search():
                with DDGS() as ddgs:
                    results = list(ddgs.text(query, max_results=max_results))
                return results
            
            results = asyncio.run(with_timeout(_search(), 15.0))
            
            formatted_results = []
            for result in results:
                formatted_results.append({
                    'title': result.get('title', ''),
                    'body': result.get('body', ''),
                    'href': result.get('href', ''),
                    'source': 'web_search'
                })
            
            logger.info(f"Found {len(formatted_results)} web results")
            return formatted_results
            
        except Exception as e:
            logger.error(f"Web search failed: {e}")
            return []
    
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
