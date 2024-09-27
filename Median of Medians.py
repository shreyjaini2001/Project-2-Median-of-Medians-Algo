import random
import time
import statistics
import matplotlib.pyplot as plt

def quickselect_median_of_medians(array, lower, higher, k):
    if higher - lower + 1 <= 5:
        return sorted(array[lower:higher+1])[k-lower]
    
    medians = []
    for i in range(lower, higher + 1, 5):
        group = sorted(array[i:min(i+5, higher + 1)])
        medians.append(group[len(group) // 2])
    
    # Recursively find the median of the medians
    median_of_medians_value = quickselect_median_of_medians(medians, 0, len(medians) - 1, len(medians) // 2)
    
    # Partition the array around the median of medians
    pivot_index = array.index(median_of_medians_value)
    array[pivot_index], array[higher] = array[higher], array[pivot_index]
    pivot_value = array[higher]
    i = lower
    for j in range(lower, higher):
        if array[j] < pivot_value:
            array[i], array[j] = array[j], array[i]
            i += 1
    array[i], array[higher] = array[higher], array[i]
    partition_index = i
    
    # Recursive cases to find the k-th smallest element
    if k == partition_index:
        return array[k]
    elif k < partition_index:
        return quickselect_median_of_medians(array, lower, partition_index - 1, k)
    else:
        return quickselect_median_of_medians(array, partition_index + 1, higher, k)

# QuickSelect call for finding the k-th smallest element
def quickselect(arr, k):
    return quickselect_median_of_medians(arr, 0, len(arr) - 1, k)

# Function to run each test case
def run_test_case(n, k):
    arr = [random.randint(0, 2100000) for _ in range(n)]
    start_time = time.time()
    result = quickselect(arr, k)
    end_time = time.time()
    return end_time - start_time

# Test cases
test_cases = [
    (4000, 50),      # Test Case 1: n = 4000, find the 50th smallest element
    (10000, 250),    # Test Case 2: n = 10000, find the 250th smallest element
    (90000, 500),    # Test Case 3: n = 90000, find the 500th smallest element
    (150000, 2500),  # Test Case 4: n = 150000, find the 2500th smallest element
    (2100000, 5000), # Test Case 5: n = 2100000, find the 5000th smallest element
]

exp_times = []
theo_times = []
adjusted_theo = []
n_values = []

for n, k in test_cases:
    time_taken = run_test_case(n, k)
    exp_times.append(time_taken*1000000000)
    theo_times.append(n)
    n_values.append(n)

avg_th = statistics.mean(theo_times) 
avg_ex = statistics.mean(exp_times)
scaling = avg_ex / avg_th
print(f"Avg th:{avg_th}")
print(f"Avg ex:{avg_ex}")
print(f"Scaling:{scaling}")


for i in range(len(exp_times)):
    adjusted_theo.append( scaling * theo_times[i])

# Print results
print(f"Experimental times: {exp_times}/n")
print(f"Theoretical times: {theo_times}")
print(f"Adjusted Theoretical times: {adjusted_theo}")

# Plotting
plt.figure(figsize=(10, 6))

# Plotting theoretical times
plt.plot(n_values, adjusted_theo, label="Adjusted Theoretical Time", marker='o')

# Plotting experimental times
plt.plot(n_values, exp_times, label="Experimental Time", marker='x')

# Logarithmic scale for better comparison
plt.xscale('log')
plt.yscale('log')

plt.xlabel("n")
plt.ylabel("Time (in ns)")
plt.title("Comparison of Adjusted Theoretical and Experimental Time Complexity")
plt.legend()

# Show the plot
plt.show()

