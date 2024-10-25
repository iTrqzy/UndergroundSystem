import pandas as pd
from adjacency_list_graph import AdjacencyListGraph
from mst import kruskal, print_undirected_edges, get_total_weight

def load_data(file_path):  # Load the London Underground data from Excel and remove rows missing journey times.
    data = pd.read_excel(file_path)
    data.columns = ['Line', 'Start Station', 'End Station', 'Journey Time']
    data = data.dropna(subset=['Journey Time'])  # Remove rows with missing journey times
    return data

def build_graph(data):  # Create a graph where each station is a node and each connection is an edge
    stations = list(set(data['Start Station']).union(set(data['End Station'])))  # Create a unique list of stations

    station_to_index = {}  # Map each station to an index
    for index, station in enumerate(stations):
        station_to_index[station] = index

    graph = AdjacencyListGraph(len(stations), weighted=True, directed=False)  # Initialize the graph
    edges = []  # List to hold edges

    for _, row in data.iterrows():  # Add each connection (edge) to the graph
        start = station_to_index[row['Start Station']]
        end = station_to_index[row['End Station']]
        journey_time = row['Journey Time']

        if graph.has_edge(start, end) == False:  # Add the edge only if it does not already exist
            graph.insert_edge(start, end, journey_time)
            edges.append((start, end, journey_time))

    return graph, edges, stations

def find_redundant_connections(graph, edges, stations):  # Identify essential connections using Kruskal's algorithm
    mst = kruskal(graph)  # Generate the Minimum Spanning Tree (MST)

    removable_connections = []  # Initialize a list to hold removable connections

    for start, end, _ in edges:  # Check each edge in the original list of edges
        if not mst.has_edge(start, end):  # If the edge is not in the MST, it can be removed
            removable_connections.append((stations[start], stations[end]))

    return removable_connections, mst

if __name__ == "__main__":
    file_path = 'London Underground Data.xlsx'

    data = load_data(file_path)  # Load and prepare the data
    graph, edges, stations = build_graph(data)  # Build the graph from the data

    removable_routes, mst = find_redundant_connections(graph, edges, stations)  # Find connections that could be removed

    print("Connections That Can Be Removed:")  # Display the removable connections
    for start, end in removable_routes:
        print(f"{start} - {end}")

    print("\nEssential Connections (MST):")  # Display the essential connections in the MST
    print_undirected_edges(mst, stations)
    total_time = get_total_weight(mst)  # Calculate the total journey time of essential connections
    print(f"\nTotal Journey Time of Essential Connections: {total_time}")