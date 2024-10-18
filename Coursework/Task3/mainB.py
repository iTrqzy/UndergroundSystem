import pandas as pd
import matplotlib.pyplot as plt
from dijkstra import dijkstra  # Import the Dijkstra function


# Step 1: Build the graph as a dictionary with journey durations as edge weights
def build_graph(london_underground_data):
    graph = {}
    stations = london_underground_data.iloc[:, 1].dropna().unique()
    station_indices = {station: i for i, station in enumerate(stations)}

    for _, row in london_underground_data.iterrows():
        station1 = row['Station1']
        station2 = row['Station2']
        duration = row['Journey_Duration']

        if station1 in station_indices and station2 in station_indices:
            current_idx = station_indices[station1]
            next_idx = station_indices[station2]

            # Add connections bidirectionally with journey duration as the weight
            if current_idx not in graph:
                graph[current_idx] = []
            if next_idx not in graph:
                graph[next_idx] = []

            graph[current_idx].append((next_idx, duration))  # Use journey duration as weight
            graph[next_idx].append((current_idx, duration))

    return graph, stations


# Step 2: Create a minimal wrapper to provide the required methods for Dijkstra
class MinimalGraphWrapper:
    def __init__(self, graph):
        self.graph = graph

    def get_card_V(self):
        return len(self.graph)  # Return the number of vertices

    def get_adj_list(self, u):
        return [Edge(v, w) for v, w in self.graph.get(u, [])]


class Edge:
    def __init__(self, v, weight):
        self.v = v
        self.weight = weight

    def get_v(self):
        return self.v

    def get_weight(self):
        return self.weight


# Step 3: Reconstruct the path using the predecessor list
def reconstruct_path(pi, source, destination, stations):
    path = []
    current = destination
    while current != source:
        path.append(stations[current])
        current = pi[current]
    path.append(stations[source])
    path.reverse()  # Reverse to get the correct order
    return path


# Step 4: Find the longest journey by time (minutes)
def find_longest_journey(graph, stations):
    wrapped_graph = MinimalGraphWrapper(graph)
    longest_journey = {'distance': 0, 'path': []}

    for station_index, station_name in enumerate(stations):
        d, pi = dijkstra(wrapped_graph, station_index)  # Run Dijkstra from this station

        # Check all destinations to find the longest journey by time
        for destination_index, distance in enumerate(d):
            if distance != float('inf') and distance > longest_journey['distance']:
                # Found a longer journey, reconstruct the path
                path = reconstruct_path(pi, station_index, destination_index, stations)
                longest_journey['distance'] = distance
                longest_journey['path'] = path

    return longest_journey


# Step 5: Load the London Underground data and build the graph
file_path = 'London Underground data.xlsx'
london_underground_data = pd.read_excel(file_path, sheet_name='Sheet1')

# Rename columns appropriately
london_underground_data.columns = ["Line", "Station1", "Station2", "Journey_Duration"]

# Step 6: Clean the data by removing rows with missing journey durations
cleaned_data = london_underground_data.dropna(subset=["Station2", "Journey_Duration"]).copy()

# Step 7: Build the graph with journey durations as weights
graph, stations = build_graph(cleaned_data)

# Step 8: Find the longest journey by time and print the results
longest_journey_info = find_longest_journey(graph, stations)

print(f"Longest journey takes {longest_journey_info['distance']} minutes.")
print(f"Path: {' -> '.join(longest_journey_info['path'])}")
