import subprocess
import time
import threading
import psutil
import argparse

def run_client_test(num_requests, num_threads, verbose):
    """
    Runs the client.py script once while concurrently measuring CPU usage.
    
    Arguments:
        num_requests (int): Number of requests to send (passed to client.py).
        num_threads (int): Number of concurrent threads (passed to client.py).
        verbose (str): Verbose flag ("true" or "false") (passed to client.py).
        
    Returns:
        elapsed_time (float): Total time taken for the client.py execution.
        avg_cpu_usage (float): Average CPU usage over the duration.
        cpu_samples (list): List of individual CPU usage samples during the run.
        client_output (str): Output from client.py.
    """
    cpu_samples = []
    stop_event = threading.Event()
    sample_interval = 0.25  # sample CPU usage every 0.5 seconds

    def monitor_cpu():
        # Warm-up call for CPU measurement.
        psutil.cpu_percent(interval=0.1)
        # Continuously sample overall CPU usage until told to stop.
        while not stop_event.is_set():
            usage = psutil.cpu_percent(interval=sample_interval)
            cpu_samples.append(usage)

    # Start the CPU monitoring thread.
    monitor_thread = threading.Thread(target=monitor_cpu)
    monitor_thread.start()

    # Start the client.py test.
    start_time = time.time()
    result = subprocess.run(
        ["python3", "client.py", str(num_requests), str(num_threads), verbose],
        capture_output=True, text=True
    )
    end_time = time.time()

    # Stop the CPU monitoring.
    stop_event.set()
    monitor_thread.join()

    elapsed_time = end_time - start_time
    avg_cpu_usage = sum(cpu_samples) / len(cpu_samples) if cpu_samples else 0

    return elapsed_time, avg_cpu_usage, cpu_samples, result.stdout

def main():
    # Parse command-line arguments.
    parser = argparse.ArgumentParser(
        description="Benchmark client.py load testing script with CPU usage metrics."
    )
    parser.add_argument("num_requests", type=int, help="Number of requests to send (for client.py)")
    parser.add_argument("num_threads", type=int, help="Number of concurrent threads (for client.py)")
    parser.add_argument("verbose", choices=["true", "false"], help="Verbose output flag (for client.py)")
    parser.add_argument("--runs", type=int, default=1, help="Number of benchmark runs (default: 10)")
    
    args = parser.parse_args()

    num_runs = args.runs
    run_times = []
    cpu_averages = []
    cpu_samples_list = []
    verbose = args.verbose == "true"

    if verbose:
        print("Starting benchmarking...\n")


    for i in range(num_runs):
        if verbose:
            print(f"=== Run {i + 1}/{num_runs} ===")

        elapsed, avg_cpu, samples, output = run_client_test(args.num_requests, args.num_threads, args.verbose)
        run_times.append(elapsed)
        cpu_averages.append(avg_cpu)
        cpu_samples_list.append(samples)

        if verbose:
            print(f"Run {i + 1}:")
            print(f"  Time Elapsed: {elapsed:.2f} seconds")
            print(f"  Average CPU Usage: {avg_cpu:.2f}%")
            # Optionally, display the client.py output:
            # print("Client output:")
            # print(output)
            print()

    overall_avg_time = sum(run_times) / len(run_times)
    overall_avg_cpu = sum(cpu_averages) / len(cpu_averages)

    if verbose:  
        print("")
        print("=== Benchmark Summary ===")
        print("Individual run times (sec):", [f"{t:.2f}" for t in run_times])
        print("Individual CPU averages (%):", [f"{cpu:.2f}" for cpu in cpu_averages])
        print("")
        print(f"Overall average time: {overall_avg_time:.2f} seconds\n")
        print(f"Overall average CPU usage: {overall_avg_cpu:.2f}%\n")
    

    print(f"Overall average time: {overall_avg_time:.2f} seconds\n")
    print(f"Overall average CPU usage: {overall_avg_cpu:.2f}%\n")
    print('-----------------------------------------------------')

    # print("Detailed CPU usage samples for each run:")
    # for i, samples in enumerate(cpu_samples_list, start=1):
    #     print(f"  Run {i}: {samples}")

if __name__ == "__main__":
    main()
