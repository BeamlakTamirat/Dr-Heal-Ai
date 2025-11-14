import requests
import time
import json

BASE_URL = "http://127.0.0.1:8000"

def test_health_endpoints():
    print("=== Testing Health Endpoints ===")
    
    # Basic health
    response = requests.get(f"{BASE_URL}/api/health")
    print(f"Basic Health: {response.status_code} - {response.json()}")
    
    # Detailed health
    response = requests.get(f"{BASE_URL}/api/health/detailed")
    print(f"Detailed Health: {response.status_code}")
    print(json.dumps(response.json(), indent=2))

def test_performance_metrics():
    print("\n=== Testing Performance Metrics ===")
    
    # Make multiple requests
    for i in range(5):
        start = time.time()
        response = requests.get(f"{BASE_URL}/api/health")
        end = time.time()
        
        process_time = response.headers.get('X-Process-Time', 'N/A')
        print(f"Request {i+1}: {response.status_code} - Process Time: {process_time}s - Actual: {end-start:.4f}s")
    
    # Check detailed metrics
    response = requests.get(f"{BASE_URL}/api/health/detailed")
    metrics = response.json().get('metrics', {})
    print(f"\nAverage Response Time: {metrics.get('avg_response_time', 0):.4f}s")
    print(f"Total Requests: {metrics.get('total_requests', 0)}")

def test_rate_limiting():
    print("\n=== Testing Rate Limiting ===")
    
    # Make rapid requests to test rate limiting
    for i in range(105):  # Exceed 100 req/min limit
        response = requests.get(f"{BASE_URL}/api/health")
        if response.status_code == 429:
            print(f"Rate limit hit at request {i+1}: {response.status_code}")
            print(f"Rate limit headers: {dict(response.headers)}")
            break
        elif i % 20 == 0:
            print(f"Request {i+1}: {response.status_code}")

if __name__ == "__main__":
    try:
        test_health_endpoints()
        test_performance_metrics()
        test_rate_limiting()
        print("\n✅ All tests completed!")
    except Exception as e:
        print(f"❌ Test failed: {e}")
