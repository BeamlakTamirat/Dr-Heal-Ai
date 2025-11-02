import time
from collections import defaultdict
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Dict, Tuple
import logging

logger = logging.getLogger(__name__)


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, calls: int = 100, period: int = 60):
        
        super().__init__(app)
        self.calls = calls
        self.period = period
        self.clients: Dict[str, list] = defaultdict(list)
    
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        
        if request.url.path in ["/health", "/", "/docs", "/openapi.json"]:
            return await call_next(request)
        
        now = time.time()
        
        self.clients[client_ip] = [
            timestamp for timestamp in self.clients[client_ip]
            if now - timestamp < self.period
        ]
        
        if len(self.clients[client_ip]) >= self.calls:
            logger.warning(f"Rate limit exceeded for {client_ip}")
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded. Maximum {self.calls} requests per {self.period} seconds."
            )
        
        self.clients[client_ip].append(now)
        
        response = await call_next(request)
        
        response.headers["X-RateLimit-Limit"] = str(self.calls)
        response.headers["X-RateLimit-Remaining"] = str(
            self.calls - len(self.clients[client_ip])
        )
        response.headers["X-RateLimit-Reset"] = str(
            int(now + self.period)
        )
        
        return response