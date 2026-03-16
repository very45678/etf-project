
import requests
import sys
import time

BASE_URL = 'http://127.0.0.1:5001'

def test_endpoint(endpoint):
    url = f"{BASE_URL}{endpoint}"
    print(f"Testing {url}...")
    try:
        start_time = time.time()
        response = requests.get(url)
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Time: {duration:.4f} seconds")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response Status: {data.get('status')}")
            print(f"Data Count: {len(data.get('data', []))}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Exception: {e}")
    print("-" * 50)

if __name__ == '__main__':
    print("Running API tests...")
    endpoints = [
        '/api/funds',
        '/api/prices?fund_code=511880',
        '/api/nav?fund_code=511880',
        '/api/yields?fund_code=511880',
        '/api/alerts',
        '/api/errors'
    ]
    
    for ep in endpoints:
        test_endpoint(ep)
    print("API tests completed.")
