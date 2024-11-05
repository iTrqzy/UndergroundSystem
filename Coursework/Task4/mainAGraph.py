import pandas as pd
import matplotlib.pyplot as plt
from adjacency_list_graph import AdjacencyListGraph
from mst import kruskal, get_total_weight
from dijkstra import dijkstra  # Assuming Dijkstra's algorithm is available in a module

def load_data(file_path):  # Load the London Underground data from Excel and remove rows missing journey times.
    data = pd.read_excel(file_path)
    data.columns = ['Line', 'Start Station', 'End Station', 'Journey Time']
    data = data.dropna(subset=['Journey Time'])  # Remove rows with missing journey times
    return data

def build_graph(data):  # Create a graph where each station is a node and each connection is an edge
    stations = list(set(data['Start Station']).union(set(data['End Station'])))  # Create a unique list of stations

    station_to_index = {station: index for index, station in enumerate(stations)}
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

def get_mst_journey_times(mst, num_stations):
    journey_times = []

    # Run Dijkstra's algorithm on the MST from each station to find all-pairs shortest paths
    for start in range(num_stations):
        distances, _ = dijkstra(mst, start)
        # Collect journey times from the shortest paths
        journey_times.extend([dist for dist in distances if dist != float('inf') and dist > 0])

    return journey_times

def plot_journey_distribution(journey_times):  # Plot a histogram of journey times
    plt.figure(figsize=(10, 6))
    plt.hist(journey_times, bins=range(0, int(max(journey_times)) + 1), color='steelblue', edgecolor='black', linewidth=0.5)
    plt.title('Histogram of Possible Journey Durations by Minutes (MST)')
    plt.xlabel('Journey Duration (Minutes)')
    plt.ylabel('Frequency')
    plt.show()

if __name__ == "__main__":
    file_path = 'London Underground Data.xlsx'

    # Load and prepare the data
    data = load_data(file_path)

    # Build the full graph from the data
    graph, edges, stations = build_graph(data)

    # Generate the MST and get essential connections only
    mst = kruskal(graph)
    num_stations = len(stations)

    # Extract journey times by finding shortest paths on the MST
    journey_times = get_mst_journey_times(mst, num_stations)

    # Plot the histogram of journey durations
    plot_journey_distribution(journey_times)
