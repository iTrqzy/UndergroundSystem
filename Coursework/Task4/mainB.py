import pandas as pd
from dijkstra import dijkstra  # Custom Dijkstra function
from adjacency_list_graph import AdjacencyListGraph
from mst import kruskal
from print_path import print_path  # Function to print the journey path

def load_data(file_path):  # Load and clean the London Underground data
    data = pd.read_excel(file_path)
    data.columns = ['Line', 'Start Station', 'End Station', 'Journey Time']
    data = data.dropna(subset=['Journey Time'])  # Remove rows with missing journey times
    return data

def build_graph(data):  # Build a graph where stations are nodes and connections are edges
    stations = list(set(data['Start Station']).union(set(data['End Station'])))  # Create a unique list of stations
    station_to_index = {station: index for index, station in enumerate(stations)}  # Map each station to an index
    graph = AdjacencyListGraph(len(stations), weighted=True, directed=False)  # Initialize the graph
    edges = []  # List to hold edges

    for _, row in data.iterrows():  # Add each connection (edge) to the graph
        start = station_to_index[row['Start Station']]
        end = station_to_index[row['End Station']]
        journey_time = row['Journey Time']

        if not graph.has_edge(start, end):  # Add the edge only if it does not already exist
            graph.insert_edge(start, end, journey_time)
            edges.append((start, end, journey_time))

    return graph, edges, stations

def find_longest_journey_mst(mst, stations, station_indices):  # Find the longest journey using the MST
    max_distance = -1  # Initialize to a very low number
    longest_path = None
    source_station = None
    target_station = None

    # Try Dijkstra's from every station and check the longest journey
    for start_idx in range(len(stations)):
        distances, predecessors = dijkstra(mst, start_idx)

        # Check all distances to find the farthest reachable station
        for end_idx, distance in enumerate(distances):
            if distance > max_distance and distance != float('inf'):
                max_distance = distance
                source_station = start_idx
                target_station = end_idx
                longest_path = print_path(predecessors, source_station, target_station, lambda idx: stations[idx])

    return max_distance, longest_path

if __name__ == "__main__":
    file_path = 'London Underground Data.xlsx'

    # Step 1: Load the data and build the full graph
    data = load_data(file_path)
    graph, edges, stations = build_graph(data)

    # Step 2: Find the Minimum Spanning Tree (MST) and get the reduced stop network
    mst = kruskal(graph)

    # Step 3: Map stations to indices for easier lookup
    station_to_index = {station: index for index, station in enumerate(stations)}

    # Step 4: Use Dijkstra's algorithm on the reduced MST network to find the longest journey
    longest_duration, longest_path = find_longest_journey_mst(mst, stations, station_to_index)

    print(f"Longest Journey Duration: {longest_duration} minutes")
    print(f"Path: {' → '.join(longest_path)}")
