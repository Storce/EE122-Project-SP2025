import requests
import time
from concurrent.futures import ThreadPoolExecutor

def send_request(url):
    try:
        response = requests.get(url)
        return response.status_code, response.elapsed.total_seconds()
    except Exception as e:
        # In a real-world scenario, you might log the exception
        return None, None

def load_test(url, num_requests=10, num_threads=5):
    print(f"Starting load test: {num_requests} requests using {num_threads} threads.")
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(send_request, url) for _ in range(num_requests)]
        results = [future.result() for future in futures]
    return results

if __name__ == '__main__':
    url = "http://localhost:5000/"
    start_time = time.time()
    results = load_test(url)
    end_time = time.time()

    # Summary statistics
    successful = [r for r in results if r[0] == 200]
    print(f"Total requests: {len(results)}")
    print(f"Successful responses: {len(successful)}")
    print(f"Total time for load test: {end_time - start_time:.2f} seconds")
