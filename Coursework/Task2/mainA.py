from Coursework.Task1.Task1CLRS.floyd_warshall import floyd_warshall
import numpy as np

NA = float("inf")  # For nodes (Stations) that have no direct connections with each other

"""
Using the code from Task1, change the matrix to show 
------------------------------
Train Station Connections    - 
------------------------------
    A     B     C     D     E -
A   0     1     ∞     1     ∞ -
B   1     0     1     ∞     ∞ -
C   ∞     1     0     1     ∞ -
D   1     ∞     1     0     1 -
E   ∞     ∞     ∞     1     0 -
------------------------------
"""

# Updated matrix where each value represents the number of stops (1 for direct connections)
train_stations_stops = np.array([  # Create an array that holds the number of stops between stations
    [0, 1, NA, 1, NA],  # Station A
    [1, 0, 1, NA, NA],  # Station B
    [NA, 1, 0, 1, NA],  # Station C
    [1, NA, 1, 0, 1],  # Station D
    [NA, NA, NA, 1, 0]  # Station E
])

# Use Floyd-Warshall to calculate the shortest path in terms of number of stops
shortest_paths_stops = floyd_warshall(train_stations_stops, len(train_stations_stops))

# Output the shortest paths between stations in terms of number of stops
print("Shortest paths in terms of number of stops:")
print(shortest_paths_stops)

