import pandas as pd
from dijkstra import dijkstra  # Import the Dijkstra function from your module

# Load data from the Excel file
file_path = 'London Underground data.xlsx'
data = pd.read_excel(file_path, sheet_name=None)  # Load all sheets
station_data = data['Sheet1']  # Use only the first sheet

# Clean the data by dropping any rows with missing values
clean_data = station_data.dropna()

# Rename columns for easier access
clean_data.columns = ["Line", "From_Station", "To_Station", "Journey_Time"]

# Create a graph as an adjacency list to represent the stations and their connections
graph = {}
all_journeys = []  # List to store all the journeys

# Loop through each row of the data to build the graph and list of journeys
for _, row in clean_data.iterrows():
    if row['From_Station'] not in graph:
        graph[row['From_Station']] = []  # Add a new station node if it's not already in the graph
    # Add the connection and journey time to the graph
    graph[row['From_Station']].append((row['To_Station'], row['Journey_Time']))

    # Add each journey to the all_journeys list
    all_journeys.append((row['From_Station'], row['To_Station'], row['Journey_Time']))

# Variables to store the longest journey
longest_path = None
longest_time = 0

# Find the longest journey by comparing journey times
for from_station, to_station, time in all_journeys:
    if time > longest_time:
        longest_time = time
        longest_path = (from_station, to_station, time)

# Print the details of the longest journey if found
if longest_path:
    print(f'Longest Journey: From {longest_path[0]} to {longest_path[1]} - Duration: {longest_path[2]} minutes.')

if __name__ == "__main__":
    # Pick the first station in the graph as the starting point
    starting_station = list(graph.keys())[0]

    if starting_station in graph:
        # Run Dijkstra's algorithm from the starting station
        distances, time = dijkstra(graph, starting_station)

        # Print the shortest distances and paths from the starting station
        for station in graph.keys():
            print(f"Station: {station}, Distance: {distances[station]}, Predecessor: {time[station]}")
