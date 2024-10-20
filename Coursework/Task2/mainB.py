import numpy as np
import random
import time
import matplotlib.pyplot as plt
from Coursework.Task1.Task1CLRS.floyd_warshall import floyd_warshall

# Define infinity to represent stations that aren't directly connected
NA = float("inf")

# Function to generate a matrix that represents the number of stops between stations
def generate_stops_matrix(number_of_stations):
    # Create an n x n matrix filled with infinity (disconnected stations)
    stops_matrix = np.full((number_of_stations, number_of_stations), NA)
    # Set the diagonal to 0 (no stops from a station to itself)
    np.fill_diagonal(stops_matrix, 0)
    return stops_matrix

# Populate the matrix with random connections, assigning 1 stop between connected stations
def populate_stops_matrix(matrix, connection_density=0.3):
    for i in range(len(matrix)):
        for j in range(i + 1, len(matrix)):
            if random.random() < connection_density:  # Connect stations with a certain probability
                matrix[i][j] = matrix[j][i] = 1  # Set 1 stop for connected stations, keep it symmetric
    return matrix

# Measure the time it takes to run Floyd-Warshall on a network of a given size, based on stops
def measure_execution_time_stops(network_size, runs=3):
    total_time = 0

    for _ in range(runs):
        # Generate the station matrix and fill it with random connections
        matrix = generate_stops_matrix(network_size)
        populated_matrix = populate_stops_matrix(matrix)

        # Start the timer, run Floyd-Warshall, and calculate the time taken
        start_time = time.time()
        floyd_warshall(populated_matrix, len(populated_matrix))
        total_time += time.time() - start_time

    # Return the average time in minutes, rounded to 5 decimal places
    avg_time = total_time / runs
    return round(avg_time / 60, 5)

# Main execution
if __name__ == "__main__":
    execution_times = []  # Store the execution times
    test_cases = [1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000]  # Test with different network sizes

    # Run tests for each network size and calculate average execution times
    for size in test_cases:
        avg_time = measure_execution_time_stops(size)
        execution_times.append(avg_time)
        print(f"Average execution time for {size} stations (based on stops): {avg_time} minutes")

    # Theoretical O(n^3) complexity for comparison
    theoretical_times = [(n ** 3) / 10 ** 7 for n in test_cases]

    # Plot the empirical data vs the theoretical time complexity
    plt.plot(test_cases, execution_times, 'bo-', label='Empirical Time (Stops)')
    plt.plot(test_cases, theoretical_times, 'r--', label="Theoretical O(n^3)")

    # Add labels and title to the plot
    plt.xlabel('Number of Stations (n)')
    plt.ylabel('Average Execution Time (minutes)')
    plt.title('Floyd-Warshall: Empirical vs Theoretical Time (Shortest Path by Stops)')
    plt.grid(True)
    plt.legend()

    # Show the plot
    plt.show()
