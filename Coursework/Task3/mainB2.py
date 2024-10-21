import pandas as pd
from dijkstra import dijkstra  # Import the Dijkstra function from your module
from adjacency_list_graph import AdjacencyListGraph

# Load data from the Excel file
file_path = 'London Underground data.xlsx'
data = pd.read_excel(file_path, sheet_name=None)  # Load all sheets into a dictionary
station_data = data['Sheet1']  # Work with the first sheet of the data

# Clean the data by removing rows with any missing values
cleaned_data = station_data.dropna()

# Rename columns for easier reference
cleaned_data.columns = ["Line", "From_Station", "To_Station", "Journey_Time"]

# Create a unique mapping of station names to indices without using enumerate
unique_stations = list(pd.concat([cleaned_data['From_Station'], cleaned_data['To_Station']]).unique())
station_to_index = {}
for i in range(len(unique_stations)):
    station_to_index[unique_stations[i]] = i

# Initialize the graph using an adjacency list representation
num_stations = len(unique_stations)
graph = AdjacencyListGraph(num_stations, directed=True, weighted=True)

# Build the graph by adding edges based on the cleaned data
for index, row in cleaned_data.iterrows():  # Use 'index' instead of '_'
    start_station_idx = station_to_index[row['From_Station']]
    end_station_idx = station_to_index[row['To_Station']]

    # Avoid adding duplicate edges
    if not any(edge.get_v() == end_station_idx for edge in graph.get_adj_list(start_station_idx)):
        graph.insert_edge(start_station_idx, end_station_idx, 1)  # Each edge represents a single stop

# Step 1: Find the longest journey by calculating journey durations using Dijkstra's algorithm
journey_lengths = []

# Calculate journey lengths (in terms of number of stops) for all station pairs
# This nested loop structure allows us to consider every possible pair of stations
for index1 in range(num_stations):  # Iterate over all stations as potential starting points
    distances, predecessors = dijkstra(graph, index1)  # Run Dijkstra's algorithm from the current starting station
    for index2 in range(num_stations):  # Iterate over all stations as potential ending points
        # Check if the distance to the current ending station is not reachable
        # and if the starting and ending stations are not the same
        if distances[index2] != float('inf') and index1 != index2:
            # Append the journey length (in terms of number of stops) and the starting/ending station indices to the list
            journey_lengths.append((distances[index2], index1, index2))

# Function to extract the first element of a tuple (for max comparison)
def get_length(journey):
    return journey[0]

# Identify the longest journey based on the number of stops using the defined function
longest_journey_length, longest_start_station, longest_end_station = max(journey_lengths, key=get_length)

# Reconstruct the path for the longest journey using Dijkstra's predecessor list
distances, predecessors = dijkstra(graph, longest_start_station)

# Build the path from the predecessor information
longest_path = []
current_station = longest_end_station

while current_station is not None:
    longest_path.append(unique_stations[current_station])
    current_station = predecessors[current_station]

# Reverse the path to display it from start to end
longest_path.reverse()

# Output the longest journey duration (in stops) and its path
print(f"Longest Journey (in stops): {longest_journey_length} stops")
print(f"Path: {' → '.join(longest_path)}")

# Step 2: Use Dijkstra's algorithm to find the shortest path from the first station
if __name__ == "__main__":
    # Choose the first station in the list as the starting point
    first_station = list(station_to_index.keys())[0]
    first_station_index = station_to_index[first_station]

    # Run Dijkstra's algorithm from the starting station
    distances, predecessors = dijkstra(graph, first_station_index)