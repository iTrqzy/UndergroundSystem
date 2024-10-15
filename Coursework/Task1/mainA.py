from Coursework.Task1.Task1CLRS.floyd_warshall import floyd_warshall
import numpy as np

NA = float("inf") # For nodes (Stations) that have no connections with each other

"""
------------------------------
Train Station Connections    - 
------------------------------
    A     B     C     D     E -
A   0     6     ∞    12     ∞ -
B   6     0     4     ∞     ∞ -
C   ∞     4     0     8     ∞ -
D   12    ∞     8     0     3 -
E   ∞     ∞     ∞     3     0 -
------------------------------
"""

train_stations = np.array([ # Create an array that holds the different stations
    [0,6,NA,12,NA], # Station: A
    [6,0,4,NA,NA], # Station: B
    [NA,4,0,8,NA], # Station: C
    [12,NA,8,0,3], # Station: D
    [NA,NA,NA,3,0] # Station: E
])

shortest_paths = floyd_warshall(train_stations,len(train_stations)) # Calls the floyd_warshall function to find -
                                                                    # the shortest path between stations
print("Shortest path in terms of minutes: ")
print(shortest_paths) # Outputs the shortest paths between the nodes