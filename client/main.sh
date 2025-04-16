#!/bin/bash

# Array of num_threads values
num_threads_values=(10 5 2)

# Loop through each value of num_threads
for num_threads in "${num_threads_values[@]}"
do
    # Run the command with current num_threads
    echo "Number of threads: $num_threads"
    python3 benchmark.py 10 $num_threads false
done
