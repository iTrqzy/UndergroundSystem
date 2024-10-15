import numpy as np
import random
import time
import matplotlib.pyplot as plt
from Coursework.Task1.Task1CLRS.floyd_warshall import floyd_warshall

# Define a constant for infinite distance between stations that have no direct connections
NA = float("inf")

# Function to generate a matrix representing the stations
# Now, instead of journey times, this will represent the number of stops
def generate_stops_matrix(number_of_stations):
    # Create an n x n matrix filled with NA (infinity) representing disconnected stations
    stops_matrix = np.full((number_of_stations, number_of_stations), NA)
    # Set the diagonal to 0 (no stops within the same station)
    np.fill_diagonal(stops_matrix, 0)
    return stops_matrix  # Return the generated matrix

# Function to populate the station matrix with random stops
# 1 stop will be added between randomly connected stations
def populate_stops_matrix(matrix, connection_density=0.3):
    for i in range(len(matrix)):
        for j in range(i + 1, len(matrix)):
            if random.random() < connection_density:  # Randomly connect stations with a certain probability
                matrix[i][j] = 1  # Add 1 stop for connected stations
                matrix[j][i] = 1  # Ensure symmetry
    return matrix

# Function to measure the execution time of the Floyd-Warshall algorithm based on number of stops
def measure_execution_time_stops(network_size, runs=3):
    total_time = 0

    for _ in range(runs):
        # Generate the matrix representing the number of stops for the given number of stations
        matrix_maker = generate_stops_matrix(network_size)
        # Populate the matrix with random stops
        station_creation = populate_stops_matrix(matrix_maker)

        # Measure the start time before running the Floyd-Warshall algorithm
        start_time = time.time()
        # Run Floyd-Warshall algorithm to calculate shortest paths based on stops
        shortest_paths = floyd_warshall(station_creation, len(station_creation))
        # Measure the time taken and accumulate it
        total_time += (time.time() - start_time)

    # Calculate the average time per run in seconds, then convert to minutes
    avg_time = total_time / runs
    avg_time_minutes = avg_time / 60
    return round(avg_time_minutes, 5)  # Return average time in minutes, rounded to 5 decimal places

# Main execution starts here
if __name__ == "__main__":
    execution_times = []  # List to store the average execution times
    test_cases = [1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000]  # Network sizes for Task 2B

    # Measure execution times for each network size (empirical data)
    for test_case in test_cases:
        avg_time = measure_execution_time_stops(test_case)  # Measure time based on number of stops
        execution_times.append(avg_time)  # Append the measured time to the execution_times list

        # Print the average execution time for this network size based on number of stops
        print(f"Average execution time for station size of {test_case} (based on stops): {avg_time} minutes")

    # Theoretical O(n^3) time complexity
    # This is the expected time complexity for Floyd-Warshall algorithm. Scaling for comparison
    theoretical_times = [(n ** 3) / 10 ** 7 for n in test_cases]

    plt.plot(test_cases, execution_times, marker='o', linestyle='-', color='b', label='Empirical Time (Stops)')

    # Plot the theoretical O(n^3) curve
    plt.plot(test_cases, theoretical_times, linestyle='--', color='r', label="Theoretical O(n^3)")

    # Add labels, title, and legend to the plot
    plt.xlabel('Number of Stations (n)')  # Set the x-axis label
    plt.ylabel('Average Execution Time (minutes)')  # Keep this as we are measuring execution time
    plt.title('Empirical vs Theoretical Time Complexity of Floyd-Warshall (Shortest Path by Stops)')  # Update the title
    plt.grid(True)  # Add grid to the plot
    plt.legend()  # Display the legend

    # Display the plot
    plt.show()

