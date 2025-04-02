import numpy as np
import time

def compute_heavy_operation(size=5):
    A = np.random.rand(size, size)
    B = np.random.rand(size, size)
    C = np.dot(A, B)
    return C

if __name__ == "__main__":
    while True:
        user_input = input("Size of matrix to compute (or type 'exit' to quit): ")
        
        if user_input.lower() == 'exit':
            print("Exiting.")
            break
        
        try:
            size = int(user_input)
            start_time = time.time()
            compute_heavy_operation(size)
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"Computation finished in {elapsed_time:.4f} seconds.\n")
        except ValueError:
            print("Please enter a valid integer or 'exit' to quit.\n")
