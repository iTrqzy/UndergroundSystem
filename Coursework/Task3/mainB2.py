import pandas as pd
from UndergroundSystem.Coursework.Task4.dijkstra import dijkstra  # Import the Dijkstra function from your custom module
from adjacency_list_graph import AdjacencyListGraph  # Import the graph implementation

# Load data from the Excel file (all sheets into a dictionary)
file = 'London Underground data.xlsx'
sheets = pd.read_excel(file, sheet_name=None)
station_data = sheets['Sheet1']  # Use the first sheet

# Clean the data by dropping rows with missing values
cleaned_data = station_data.dropna()

# Rename columns to make them easier to reference
cleaned_data.columns = ["Line", "From_Station", "To_Station", "Journey_Time"]

# Create a list of unique stations (both from 'From_Station' and 'To_Station')
stations = list(pd.concat([cleaned_data['From_Station'], cleaned_data['To_Station']]).unique())

# Create a mapping from station names to indices
station_to_index = {station: i for i, station in enumerate(stations)}

# Initialize the graph (directed and weighted)
num_stations = len(stations)
graph = AdjacencyListGraph(num_stations, directed=True, weighted=True)

# Build the graph by adding edges based on the data
for idx, row in cleaned_data.iterrows():
    start_idx = station_to_index[row['From_Station']]
    end_idx = station_to_index[row['To_Station']]

    # Avoid duplicate edges
    if not any(edge.get_v() == end_idx for edge in graph.get_adj_list(start_idx)):
        graph.insert_edge(start_idx, end_idx, 1)  # Add an edge for each stop

# Find the longest journey by calculating journey durations using Dijkstra's algorithm
journey_durations = []  # List to store journey lengths and station indices

# Calculate the journey length between all station pairs
for start in range(num_stations):
    distances, predecessors = dijkstra(graph, start)  # Run Dijkstra from the current station
    for end in range(num_stations):
        # If a valid path exists and the stations aren't the same
        if distances[end] != float('inf') and start != end:
            journey_durations.append((distances[end], start, end))  # Add the distance and station indices


# Function to get the journey length (for finding max)
def get_journey_length(journey):
    return journey[0]


# Find the longest journey (in terms of stops) and the stations involved
longest_duration, start_station_idx, end_station_idx = max(journey_durations, key=get_journey_length)

# Reconstruct the path for the longest journey using the predecessors from Dijkstra's algorithm
distances, predecessors = dijkstra(graph, start_station_idx)  # Run Dijkstra again for the longest journey's start
path = []  # List to store the longest journey path
current = end_station_idx  # Start from the end station

# Trace back from the end station to the start using the predecessor list
while current is not None:
    path.append(stations[current])
    current = predecessors[current]

# Reverse the path so it's in the correct order (from start to end)
path.reverse()

# Output the longest journey details
print(f"Longest Journey (in stops): {longest_duration} stops")
print(f"Path: {' → '.join(path)}")

# Find the shortest path from the first station
if __name__ == "__main__":
    first_station = stations[0]  # Take the first station as the starting point
    first_station_idx = station_to_index[first_station]

    # Run Dijkstra's algorithm to find the shortest paths from the first station
    distances, predecessors = dijkstra(graph, first_station_idx)
