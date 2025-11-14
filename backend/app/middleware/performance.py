import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.utils.metrics import get_metrics

class PerformanceMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.metrics = get_metrics()
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        try:
            response = await call_next(request)
            process_time = time.time() - start_time
            
            self.metrics.record_response_time(request.url.path, process_time)
            response.headers["X-Process-Time"] = str(round(process_time, 4))
            
            return response
        
        except Exception as e:
            process_time = time.time() - start_time
            self.metrics.record_error(request.url.path, type(e).__name__)
            raise e
