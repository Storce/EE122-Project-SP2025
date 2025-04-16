import requests
import time
import argparse
from concurrent.futures import ThreadPoolExecutor

def send_request(url):
    try:
        response = requests.get(url)
        return response.status_code, response.elapsed.total_seconds()
    except Exception:
        return 0, None  # Consistent format for error

def load_test(url, num_requests=10, num_threads=5):
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(send_request, url) for _ in range(num_requests)]
        results = [future.result() for future in futures]
    return results

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Simple Load Test Client")
    parser.add_argument("num_requests", type=int, help="Number of requests to send")
    parser.add_argument("num_threads", type=int, help="Number of concurrent threads")
    parser.add_argument("verbose", type=str, choices=["true", "false"], help="Verbose output (true or false)")
    args = parser.parse_args()

    verbose = args.verbose.lower() == "true"
    num_requests = args.num_requests
    num_threads = args.num_threads

    url = "http://0.0.0.0:3200/"

    if verbose:
        print(f"Starting load test on {url} with {num_requests} requests using {num_threads} threads.")

    start_time = time.time()
    results = load_test(url, num_requests, num_threads)
    end_time = time.time()

    if verbose:
        for i, (status, elapsed) in enumerate(results, start=1):
            print(f"Request {i}: Status Code={status}, Time={elapsed:.3f} sec" if elapsed is not None else f"Request {i}: Failed")

    successful = [r for r in results if r[0] == 200]
    failed = [r for r in results if r[0] != 200]

    print(f"\nTotal requests: {len(results)}")
    print(f"Successful responses: {len(successful)}")
    print(f"Failed responses: {len(failed)}")
    print(f"Total time for load test: {end_time - start_time:.2f} seconds")
