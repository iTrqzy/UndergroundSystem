import pandas as pd
from UndergroundSystem.Coursework.Task4.dijkstra import dijkstra  # Custom Dijkstra function
from adjacency_list_graph import AdjacencyListGraph
from UndergroundSystem.Coursework.Task4.print_path import print_path  # Function to print the journey path

# Load the data from the Excel file
file = 'London Underground data.xlsx'
sheets = pd.read_excel(file, sheet_name=None)  # Load all sheets
station_data = sheets['Sheet1']  # We'll work with the first sheet

# Clean the data by dropping rows with missing values
clean_data = station_data.dropna()

# Rename columns for easier access
clean_data.columns = ["Line", "From_Station", "To_Station", "Journey_Time"]

# Create a mapping of station names to indices
station_names = list(pd.concat([clean_data['From_Station'], clean_data['To_Station']]).unique())
station_indices = {name: idx for idx, name in enumerate(station_names)}

# Set up the graph (undirected and weighted since journeys are bidirectional)
num_stations = len(station_names)
graph = AdjacencyListGraph(num_stations, directed=False, weighted=True)

# Initialize a counter for the number of unique journeys
unique_journey_count = 0

# Build the graph by adding edges (connections between stations)
for _, row in clean_data.iterrows():
    from_idx = station_indices[row['From_Station']]
    to_idx = station_indices[row['To_Station']]
    journey_time = row['Journey_Time']

    # Only add the edge if it doesn't already exist to avoid duplicates
    if not graph.has_edge(from_idx, to_idx):
        graph.insert_edge(from_idx, to_idx, journey_time)
        unique_journey_count += 1  # Increment the counter for each unique journey

# Output the number of unique journeys
print(f"Number of unique journeys: {unique_journey_count}")

# Helper function to map station indices back to station names
def map_station(index):
    return station_names[index]

# Function to find the longest journey across all stations
def find_longest_journey():
    max_distance = -1  # Initialize to a very low number
    longest_path = None
    source_station = None
    target_station = None

    # Try Dijkstra's from every station and check the longest journey
    for start_idx, station_name in enumerate(station_names):
        distances, predecessors = dijkstra(graph, start_idx)

        # Check all distances to find the farthest reachable station
        for end_idx, distance in enumerate(distances):
            if distance > max_distance and distance != float('inf'):
                max_distance = distance
                source_station = start_idx
                target_station = end_idx
                longest_path = print_path(predecessors, source_station, target_station, map_station)

    return max_distance, longest_path

# Find and print the longest journey
longest_duration, longest_path = find_longest_journey()

print(f"Longest Journey Duration: {longest_duration} minutes")
print(f"Path: {' → '.join(longest_path)}")
