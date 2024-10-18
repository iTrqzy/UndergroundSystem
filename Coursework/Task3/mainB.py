import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from dijkstra import dijkstra  # Provided Dijkstra function

# Define a constant for infinite distance
NA = float('inf')

# Function to create adjacency matrix from the London Underground data
def create_adjacency_matrix(df, station_list):
    n = len(station_list)
    matrix = np.full((n, n), NA)

    station_index = {station: idx for idx, station in enumerate(station_list)}

    for _, row in df.iterrows():
        station1 = row['Station1'].strip()
        station2 = row['Station2'].strip()
        if station1 in station_index and station2 in station_index:
            idx1, idx2 = station_index[station1], station_index[station2]
            matrix[idx1][idx2] = 1  # 1 stop between stations
            matrix[idx2][idx1] = 1  # Symmetric

    np.fill_diagonal(matrix, 0)  # Set diagonal to 0 (no stop within the same station)
    return matrix, station_index

# Convert adjacency matrix to the expected graph format for Dijkstra
def convert_matrix_to_graph(matrix):
    graph = {}
    n = len(matrix)
    for i in range(n):
        graph[i] = {}
        for j in range(n):
            if matrix[i][j] != NA:
                graph[i][j] = matrix[i][j]
    return graph

# Function to find the longest path in terms of stops using the provided Dijkstra function
def find_longest_path_by_stops(matrix, station_index):
    graph = convert_matrix_to_graph(matrix)  # Convert matrix to graph format
    longest_distance = 0
    longest_path = []

    for start_station in station_index.values():
        distances, predecessors = dijkstra(graph, start_station)  # Use the provided Dijkstra function
        max_distance = max(distances)

        if max_distance < float('inf') and max_distance > longest_distance:
            longest_distance = max_distance
            end_station = np.argmax(distances)
            longest_path = reconstruct_path(predecessors, start_station, end_station, station_index)

    return longest_distance, longest_path

# Function to reconstruct the path from predecessors returned by Dijkstra
def reconstruct_path(predecessors, start, end, station_index):
    reverse_station_index = {v: k for k, v in station_index.items()}
    path = []
    while end is not None:
        path.insert(0, reverse_station_index[end])
        end = predecessors[end]
    return path

# Function to plot the histogram of journey durations (in terms of stops)
def plot_histogram(matrix):
    journey_durations = []

    graph = convert_matrix_to_graph(matrix)  # Convert the matrix to graph format
    for i in range(len(matrix)):
        distances, _ = dijkstra(graph, i)
        journey_durations.extend([d for d in distances if d < float('inf')])  # Exclude infinite values

    plt.figure(figsize=(10, 6))
    plt.hist(journey_durations, bins=20, color='blue', edgecolor='black')
    plt.title('Histogram of Journey Durations (Number of Stops)')
    plt.xlabel('Number of Stops')
    plt.ylabel('Frequency')
    plt.show()

# Load the London Underground data
file_path = 'London Underground data.xlsx'
data = pd.read_excel(file_path, sheet_name='Sheet1')
data.columns = ["Line", "Station1", "Station2", "Journey_Duration"]

# Drop rows with NaN values
cleaned_data = data.dropna()

# Get a unique list of stations
stations = pd.concat([cleaned_data['Station1'], cleaned_data['Station2']]).unique()

# Create the adjacency matrix based on stops
stops_matrix, station_index = create_adjacency_matrix(cleaned_data, stations)

# Find the longest journey by number of stops
longest_distance, longest_path = find_longest_path_by_stops(stops_matrix, station_index)
print(f"Longest journey is {longest_distance} stops long, path: {longest_path}")

# Plot histogram of the number of stops
plot_histogram(stops_matrix)
