import pandas as pd
import matplotlib.pyplot as plt
from adjacency_list_graph import AdjacencyListGraph
from UndergroundSystem.Coursework.Task4.dijkstra import dijkstra

# Load data from the Excel file and clean it
def load_data(file_path):
    data = pd.read_excel(file_path)
    data.columns = ['Line', 'Start Station', 'End Station', 'Journey Time']
    data = data.dropna(subset=['Journey Time'])  # Remove rows with missing journey times
    return data

# Build the initial graph with all connections
def build_graph(data):
    stations = list(set(data['Start Station']).union(set(data['End Station'])))
    station_to_index = {station: index for index, station in enumerate(stations)}
    graph = AdjacencyListGraph(len(stations), weighted=True, directed=False)

    for _, row in data.iterrows():
        start = station_to_index[row['Start Station']]
        end = station_to_index[row['End Station']]
        journey_time = row['Journey Time']
        if not graph.has_edge(start, end):  # Add only if the edge doesn't already exist
            graph.insert_edge(start, end, journey_time)

    return graph, station_to_index, stations

# Build a reduced graph with only essential connections based on shortest paths
def build_essential_graph(graph, num_stations):
    essential_graph = AdjacencyListGraph(num_stations, weighted=True, directed=False)
    journey_times = []

    # Run Dijkstra from each station to determine essential connections
    for start in range(num_stations):
        distances, predecessors = dijkstra(graph, start)
        for end in range(num_stations):
            if end != start and distances[end] != float('inf'):
                journey_time = distances[end]
                # Only add the connection if it's essential (shortest path found)
                if not essential_graph.has_edge(start, end):
                    essential_graph.insert_edge(start, end, journey_time)
                    journey_times.append(journey_time)

    return essential_graph, journey_times

# Plot a histogram of journey times
def plot_journey_distribution(journey_times):
    plt.figure(figsize=(10, 6))
    plt.hist(journey_times, bins=range(0, int(max(journey_times)) + 1), color='steelblue')
    plt.title('Histogram of Journey Times After Line Closures')
    plt.xlabel('Journey Duration (Minutes)')
    plt.ylabel('Frequency')
    plt.show()

# Main function to execute the logic
if __name__ == "__main__":
    file_path = 'London Underground data.xlsx'
    data = load_data(file_path)

    # Build the complete graph and station mappings
    graph, station_to_index, stations = build_graph(data)

    # Build the essential graph and retrieve journey times
    essential_graph, journey_times = build_essential_graph(graph, len(stations))

    # Plot the journey time distribution
    plot_journey_distribution(journey_times)
