#!/bin/bash

# Number of iterations
iterations=100

for ((i=1; i<=$iterations; i++)); do
    
    # perform dns lookup
    dig packetwarden.adhld @127.0.0.1

    # sleep for while before next iteration
    sleep 2
done