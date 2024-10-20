import numpy as np
import random
import time
import matplotlib.pyplot as plt
from Coursework.Task1.Task1CLRS.floyd_warshall import floyd_warshall

# Define constants
NA = float("inf")  # Infinite distance for stations with no direct connection
MAX_DURATION = 45  # Max journey time in minutes for random connections


# Generates an n x n matrix representing stations with no initial connections (set to infinity)
def generate_matrix(number_of_stations):
    matrix = np.full((number_of_stations, number_of_stations), NA)
    np.fill_diagonal(matrix, 0)  # Distance to itself is always zero
    return matrix


# Populates the station matrix with random journey times between stations
def populate_stations(matrix):
    for i in range(len(matrix)):
        for j in range(i + 1, len(matrix)):
            duration = random.randint(1, MAX_DURATION)
            matrix[i][j] = matrix[j][i] = duration  # Symmetrical travel times
    return matrix


# Measures the average execution time of the Floyd-Warshall algorithm over a number of runs
def measure_execution_time(network_size, runs=3):
    total_time = 0

    for _ in range(runs):
        matrix = generate_matrix(network_size)
        populated_matrix = populate_stations(matrix)

        start_time = time.time()
        floyd_warshall(populated_matrix, len(populated_matrix))
        total_time += time.time() - start_time

    avg_time = total_time / runs
    return round(avg_time / 60, 5)  # Return time in minutes, rounded to 5 decimal places


# Main block for testing different network sizes and plotting results
if __name__ == "__main__":
    test_cases = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
    execution_times = []

    for size in test_cases:
        avg_time = measure_execution_time(size)
        execution_times.append(avg_time)
        print(f"Average execution time for {size} stations: {avg_time} minutes")

    # Expected O(n^3) time complexity for comparison
    theoretical_times = [(n ** 3) / 10 ** 7 for n in test_cases]

    # Plot the results
    plt.plot(test_cases, execution_times, 'bo-', label='Empirical Time')
    plt.plot(test_cases, theoretical_times, 'r--', label="Theoretical O(n^3)")
    plt.xlabel('Number of Stations (n)')
    plt.ylabel('Average Execution Time (minutes)')
    plt.title('Floyd-Warshall: Empirical vs Theoretical Time Complexity')
    plt.grid(True)
    plt.legend()
    plt.show()
