import pandas as pd
import matplotlib.pyplot as plt
from adjacency_list_graph import AdjacencyListGraph
from mst import kruskal, get_total_weight, print_undirected_edges

def load_data(file_path):  # Load and clean the London Underground data from Excel
    data = pd.read_excel(file_path)
    data.columns = ['Line', 'Start Station', 'End Station', 'Journey Time']
    data = data.dropna(subset=['Journey Time'])  # Remove rows with missing journey times
    return data

def build_graph(data):  # Build a graph where stations are nodes and connections are edges
    stations = list(set(data['Start Station']).union(set(data['End Station'])))  # Unique stations
    station_to_index = {station: index for index, station in enumerate(stations)}  # Map stations to indices
    graph = AdjacencyListGraph(len(stations), weighted=True, directed=False)  # Initialize the graph
    edges = []  # List to store the edges

    for _, row in data.iterrows():  # Add edges for each connection in the data
        start = station_to_index[row['Start Station']]
        end = station_to_index[row['End Station']]
        journey_time = row['Journey Time']

        if not graph.has_edge(start, end):  # Add only if the edge doesn't already exist
            graph.insert_edge(start, end, journey_time)
            edges.append((start, end, journey_time))

    return graph, edges, stations

def get_edge_weight(graph, start, end):  # Get the weight (journey time) for an edge
    edge = graph.find_edge(start, end)
    if edge:
        return edge.get_weight()  # Return the weight if the edge exists
    return None  # Return None if no edge is found

def plot_journey_distribution(journey_times):  # Plot a histogram of journey durations
    plt.figure(figsize=(10, 6))
    plt.hist(journey_times, bins=range(int(min(journey_times)), int(max(journey_times)) + 1),
             color='green', edgecolor='black', align='left')
    plt.title('London Underground Journey Duration Distribution (MST)')
    plt.xlabel('Journey Duration (Minutes)')
    plt.ylabel('Frequency')
    plt.show()

if __name__ == "__main__":
    file_path = 'London Underground Data.xlsx'

    # Load the data and build the graph
    data = load_data(file_path)
    graph, edges, stations = build_graph(data)

    # Find the Minimum Spanning Tree (MST) using Kruskal's algorithm
    mst = kruskal(graph)

    # Extract journey times from the MST
    mst_edges = mst.get_edge_list()  # Get the MST edges

    journey_times = []
    for edge in mst_edges:
        if len(edge) == 3:  # Edge includes (start, end, weight)
            _, _, weight = edge
        elif len(edge) == 2:  # Edge includes only (start, end)
            start, end = edge
            weight = get_edge_weight(graph, start, end)  # Get the weight using the graph's method
        journey_times.append(weight)

    # Plot the distribution of journey durations
    plot_journey_distribution(journey_times)

    # Print the essential connections in the MST and the total journey time
    print("\nEssential Connections (MST):")
    print_undirected_edges(mst, stations)
    total_time = get_total_weight(mst)
    print(f"\nTotal Journey Time of Essential Connections: {total_time}")
