import pandas as pd
from dijkstra import dijkstra  # Import the Dijkstra function from your module


file_path = 'London Underground data.xlsx' # Load data from the Excel file
data = pd.read_excel(file_path, sheet_name=None)  # Load all sheets from the file
station_data = data['Sheet1']  # We only need the first sheet


clean_data = station_data.dropna() # Remove any rows with missing values

clean_data.columns = ["Line", "From_Station", "To_Station", "Journey_Time"] # Rename columns for easier access

graph = {} # Creating an adjacency list for the data extracted from the Excel file
all_journeys = [] # Creating an array that will hold all the journeys found

for _, row in clean_data.iterrows(): # Loops through the different rows of the Excel file
    if row['From_Station'] not in graph: # If the station is not found in the graph then create a node
        graph[row['From_Station']] = []
    graph[row['From_Station']].append((row['To_Station'], row['Journey_Time'])) # Adds the time and direction to the node


    all_journeys.append((row['From_Station'], row['To_Station'], row['Journey_Time']))     # Add the station to all_journeys array


longest_path = None # Stores the longest path and time as the program goes on
longest_time = 0

for from_station, to_station, time in all_journeys:
    if time > longest_time: # Compares the time to the next and if it is greater than, then make that the longest time
        longest_time = time
        longest_path = (from_station, to_station, time)

# Print out the details of the longest journey
if longest_path:
    print(f'Longest Journey: From {longest_path[0]} to {longest_path[1]} - Duration: {longest_path[2]} minutes.')


if __name__ == "__main__":
    # Select the first station in the graph to use as the starting point
    starting_station = list(graph.keys())[0]

    if starting_station in graph:
        distances, time = dijkstra(graph, starting_station)

        # Output the shortest distances and paths from the starting station to each other station
        for station in graph.keys():
            print(f"Station: {station}, Distance: {distances[station]}, Predecessor: {time[station]}")