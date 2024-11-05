import pandas as pd
import matplotlib.pyplot as plt
from adjacency_list_graph import AdjacencyListGraph
from UndergroundSystem.Coursework.Task4.dijkstra import dijkstra

# Load the data from the Excel file
excel_file_path = 'London Underground data.xlsx'
underground_data = pd.read_excel(excel_file_path, sheet_name='Sheet1')

# Rename columns for easier understanding
underground_data.columns = ["Line_Name", "Starting_Station", "Ending_Station", "Journey_Duration"]

# Create a list of unique stations and initialize the graph
unique_stations = list(set(underground_data["Starting_Station"].tolist() + underground_data["Ending_Station"].tolist()))
station_graph = AdjacencyListGraph(len(unique_stations), directed=False, weighted=1)

# Create a dictionary to map station names to numerical indices
station_to_index = {}
index_counter = 0  # Initialize an index counter
for station in unique_stations:
    station_to_index[station] = index_counter
    index_counter += 1  # Increment the counter for the next station

# Add connections (edges) to the graph based on journey data
for _, row in underground_data.iterrows():
    start_station_index = station_to_index[row["Starting_Station"]]
    end_station_index = station_to_index[row["Ending_Station"]]
    travel_duration = row["Journey_Duration"]

    # Only add the connection if it doesn't already exist
    if not station_graph.has_edge(start_station_index, end_station_index):
        station_graph.insert_edge(start_station_index, end_station_index, travel_duration)

# Function to reconstruct the path from the predecessors list
def reconstruct_path(predecessors_list, source_station, destination_station):
    path_trace = []
    current_station = destination_station
    while current_station != source_station:
        path_trace.insert(0, current_station)
        current_station = predecessors_list[current_station]
    path_trace.insert(0, source_station)  # Add the source station to the path
    return path_trace

# Function to calculate the number of stops between every pair of stations
def get_stops_between_all_stations(station_graph, unique_stations):
    stops_count = []
    total_stations = len(unique_stations)

    for source_station in range(total_stations):
        # Get the list of predecessors for the current source station using Dijkstra
        predecessors_list = dijkstra(station_graph, source_station)[1]

        # For each destination station, calculate the number of stops
        for destination_station in range(total_stations):
            if predecessors_list[destination_station] and source_station != destination_station:
                reconstructed_path = reconstruct_path(predecessors_list, source_station, destination_station)
                stops_count.append(len(reconstructed_path) - 1)  # Number of stops is path length - 1

    return stops_count

# Calculate the number of stops for all station pairs
stops_between_stations = get_stops_between_all_stations(station_graph, unique_stations)

# Output the total number of journey durations calculated
print(f"Total number of journey durations calculated: {len(stops_between_stations)}")

# Plot the histogram of stops
plt.figure(figsize=(10, 6))
plt.hist(stops_between_stations, bins=40, color='blue', edgecolor='black', align='left')
plt.title('Histogram of Journey Durations by Number of Stops')
plt.xlabel('Number of Stops')
plt.ylabel('Frequency')
plt.show()
