import time
from collections import defaultdict, deque
from typing import Dict, List

class MetricsCollector:
    def __init__(self):
        self.response_times = deque(maxlen=1000)
        self.error_counts = defaultdict(int)
        self.request_counts = defaultdict(int)
        self.start_time = time.time()
    
    def record_response_time(self, endpoint: str, response_time: float):
        self.response_times.append(response_time)
        self.request_counts[endpoint] += 1
    
    def record_error(self, endpoint: str, error_type: str):
        self.error_counts[f"{endpoint}:{error_type}"] += 1
    
    def get_avg_response_time(self) -> float:
        if not self.response_times:
            return 0.0
        return sum(self.response_times) / len(self.response_times)
    
    def get_stats(self) -> Dict:
        return {
            "avg_response_time": self.get_avg_response_time(),
            "total_requests": sum(self.request_counts.values()),
            "total_errors": sum(self.error_counts.values()),
            "uptime_seconds": time.time() - self.start_time,
            "recent_response_times": list(self.response_times)[-10:]
        }

_metrics = MetricsCollector()

def get_metrics() -> MetricsCollector:
    return _metrics
