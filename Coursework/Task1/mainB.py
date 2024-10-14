import numpy as np
import random
import time
import matplotlib.pyplot as plt
from Coursework.Task1.Task1CLRS.floyd_warshall import floyd_warshall

"""
--------------------------------------------------------------------------------------------------------------------
train_stations = np.array([ # Create an array that holds the different stations
    [0,6,NA,12,NA], # Station: A
    [6,0,4,NA,NA], # Station: B
    [NA,4,0,8,NA], # Station: C
    [12,NA,8,0,3], # Station: D
    [NA,NA,NA,3,0] # Station: E
])
--------------------------------------------------------------------------------------------------------------------
Steps for Task 1B:
    - Create a function that will generate a larger tube network in the format that is currently in train_stations.
    - Once that has been made determine the path and journey duration in minutes using the code from mainA.py.
    - Calculate average execution time with different network sizes using time library.
    - Calculate average execution time of network sized: 100-1000.
    - Plot the results on a graph comparing network size and its average execution time.
--------------------------------------------------------------------------------------------------------------------
"""

# Define a constant for infinite distance between stations that have no direct connections
NA = float("inf")
# Define a maximum journey duration for random station connections
MAX_DURATION = 45


# Function to generate a matrix representing the stations
def generate_matrix(number_of_stations):
    # Create an n x n matrix filled with NA (infinity) representing disconnected stations
    default_station = np.full((number_of_stations, number_of_stations), NA)
    # Set the diagonal to 0 (distance from a station to itself is 0)
    np.fill_diagonal(default_station, 0)
    return default_station  # Return the generated matrix


# Function to populate the station matrix with random journey times
def populate_stations(matrix):
    # Iterate over all pairs of stations to assign journey times
    for i in range(len(matrix)):  # Iterate through each station
        for j in range(i + 1, len(matrix)):  # Iterate through stations after station i
            station_weight = random.randint(1, MAX_DURATION)  # Generate a random journey time
            matrix[i][j] = station_weight  # Set journey time between station i and station j
            matrix[j][i] = station_weight  # Ensure symmetry: station j to station i has the same journey time
    return matrix  # Return the populated matrix


# Function to measure the execution time of the Floyd-Warshall algorithm
def measure_execution_time(network_size, runs=3):  # Increased runs for more accuracy
    total_time = 0  # Initialize the total time variable

    for _ in range(runs):
        # Generate the matrix representing the tube network for the given number of stations
        matrix_maker = generate_matrix(network_size)
        # Populate the matrix with random journey times
        station_creation = populate_stations(matrix_maker)

        # Measure the start time before running the Floyd-Warshall algorithm
        start_time = time.time()
        # Run Floyd-Warshall algorithm to calculate shortest paths
        shortest_paths = floyd_warshall(station_creation, len(station_creation))
        # Measure the time taken and accumulate it
        total_time += (time.time() - start_time)

    # Calculate the average time per run in seconds, then convert to minutes
    avg_time = total_time / runs
    avg_time_minutes = avg_time / 60  # Convert to minutes if needed
    return round(avg_time_minutes, 5)  # Return average time rounded to 5 decimal places


# Main execution starts here
if __name__ == "__main__":
    execution_times = []  # List to store the average execution times
    test_cases = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]  # Define test cases for different network sizes

    # Measure execution times for each network size (empirical data)
    for test_case in test_cases:
        avg_time = measure_execution_time(test_case)  # Measure time for Floyd-Warshall
        execution_times.append(avg_time)  # Append the measured time to the execution_times list

        # Print the average execution time for this network size
        print(f"Average execution time for station sizes of {test_case}: {avg_time} minutes")

    # Theoretical O(n^3) time complexity
    # This is the expected time complexity for Floyd-Warshall algorithm. Scaling for comparison
    theoretical_times = [(n ** 3) / 10 ** 7 for n in test_cases]  # Adjust scaling for better visual comparison

    # Plot the empirical data
    plt.plot(test_cases, execution_times, marker='o', linestyle='-', color='b', label='Empirical Time')

    # Plot the theoretical O(n^3) curve
    plt.plot(test_cases, theoretical_times, linestyle='--', color='r', label="Theoretical O(n^3)")

    # Add labels, title, and legend to the plot
    plt.xlabel('Number of Stations (n)')  # Set the x-axis label
    plt.ylabel('Average Execution Time (minutes)')  # Set the y-axis label
    plt.title('Empirical vs Theoretical Time Complexity of Floyd-Warshall Algorithm')  # Set the plot title
    plt.grid(True)  # Add grid to the plot
    plt.legend()  # Display the legend

    # Display the plot
    plt.show()
