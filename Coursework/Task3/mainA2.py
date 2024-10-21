import pandas as pd
from dijkstra import dijkstra  # Import the Dijkstra function from your module
from adjacency_list_graph import AdjacencyListGraph

# Load data from the Excel file
file_path = 'London Underground data.xlsx'
data = pd.read_excel(file_path, sheet_name=None)  # Load all sheets
station_data = data['Sheet1']  # Use only the first sheet

# Clean the data by dropping any rows with missing values
clean_data = station_data.dropna()

# Rename columns for easier access
clean_data.columns = ["Line", "From_Station", "To_Station", "Journey_Time"]

# Create a mapping of station names to indices
station_names = list(pd.concat([clean_data['From_Station'], clean_data['To_Station']]).unique())
station_indices = {name: idx for idx, name in enumerate(station_names)}

# Create the graph as an AdjacencyListGraph
num_stations = len(station_names)
graph = AdjacencyListGraph(num_stations, directed=True, weighted=True)

# Loop through each row of the data to build the graph
for _, row in clean_data.iterrows():
    from_idx = station_indices[row['From_Station']]
    to_idx = station_indices[row['To_Station']]
    journey_time = row['Journey_Time']

    # Check if the edge already exists to avoid duplicate edges
    existing_edges = graph.get_adj_list(from_idx)
    if any(edge.get_v() == to_idx for edge in existing_edges):
        print(f"Edge from {from_idx} to {to_idx} already exists. Skipping...")
        continue

    # Insert the edge into the adjacency list graph
    graph.insert_edge(from_idx, to_idx, journey_time)

# Find the longest journey by comparing journey times
longest_path = clean_data.loc[clean_data['Journey_Time'].idxmax()]
print(
    f'Longest Journey: From {longest_path["From_Station"]} to {longest_path["To_Station"]} - Duration: {longest_path["Journey_Time"]} minutes.')

if __name__ == "__main__":
    # Pick the first station in the graph as the starting point
    starting_station = list(station_indices.keys())[0]
    starting_index = station_indices[starting_station]

    # Run Dijkstra's algorithm from the starting station
    distances, predecessors = dijkstra(graph, starting_index)

    # Print the shortest distances and paths from the starting station
    for station, idx in station_indices.items():
        distance = distances[idx]
        predecessor_idx = predecessors[idx]
        predecessor = station_names[predecessor_idx] if predecessor_idx is not None else "None"
        print(f"Station: {station}, Distance: {distance}, Predecessor: {predecessor}")