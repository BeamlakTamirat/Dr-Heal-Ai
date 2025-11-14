from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
import re
import logging

logger = logging.getLogger(__name__)

class SecurityMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.sql_injection_patterns = [
            r"(\bUNION\b|\bSELECT\b|\bINSERT\b|\bDELETE\b|\bUPDATE\b|\bDROP\b)",
            r"(--|#|/\*|\*/)",
            r"(\bOR\b|\bAND\b)\s+\d+\s*=\s*\d+"
        ]
        self.xss_patterns = [
            r"<script[^>]*>.*?</script>",
            r"javascript:",
            r"on\w+\s*=",
            r"<iframe[^>]*>.*?</iframe>"
        ]
    
    async def dispatch(self, request: Request, call_next):
        if request.method in ["POST", "PUT", "PATCH"]:
            body = await request.body()
            body_str = body.decode('utf-8', errors='ignore')
            
            if self._detect_sql_injection(body_str):
                logger.warning(f"SQL injection attempt from {request.client.host}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid request content"
                )
            
            if self._detect_xss(body_str):
                logger.warning(f"XSS attempt from {request.client.host}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid request content"
                )
        
        query_params = str(request.query_params)
        if self._detect_sql_injection(query_params) or self._detect_xss(query_params):
            logger.warning(f"Malicious query params from {request.client.host}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid query parameters"
            )
        
        response = await call_next(request)
        
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        
        return response
    
    def _detect_sql_injection(self, content: str) -> bool:
        content_upper = content.upper()
        for pattern in self.sql_injection_patterns:
            if re.search(pattern, content_upper, re.IGNORECASE):
                return True
        return False
    
    def _detect_xss(self, content: str) -> bool:
        for pattern in self.xss_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                return True
        return False
