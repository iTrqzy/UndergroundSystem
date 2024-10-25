import pandas as pd
from adjacency_list_graph import AdjacencyListGraph
from mst import kruskal, print_undirected_edges, get_total_weight

def load_underground_data(file_path):
    """
    Load and clean the Excel data for the London Underground.
    Drops any rows without journey time data.
    """
    underground_data = pd.read_excel(file_path)
    underground_data.columns = ['Line', 'Start Station', 'End Station', 'Journey Time']
    cleaned_data = underground_data.dropna(subset=['Journey Time'])
    return cleaned_data

def create_station_graph(cleaned_data):
    """
    Build an adjacency list graph from the cleaned station data.
    Each unique station is a node, and connections with journey times are weighted edges.
    """
    stations = list(set(cleaned_data['Start Station']).union(set(cleaned_data['End Station'])))
    station_to_index = {station: idx for idx, station in enumerate(stations)}
    total_stations = len(stations)

    station_graph = AdjacencyListGraph(total_stations, weighted=True, directed=False)
    graph_edges = []

    for _, row in cleaned_data.iterrows():
        start_idx = station_to_index[row['Start Station']]
        end_idx = station_to_index[row['End Station']]
        journey_time = row['Journey Time']

        if not station_graph.has_edge(start_idx, end_idx):
            station_graph.insert_edge(start_idx, end_idx, journey_time)
            graph_edges.append((start_idx, end_idx, journey_time))

    return station_graph, graph_edges, stations

def find_closable_line_sections(station_graph, graph_edges, stations):
    """
    Use Kruskal's algorithm to find the Minimum Spanning Tree (MST).
    Determine which edges (line sections) can be closed without breaking connectivity.
    """
    mst = kruskal(station_graph)

    closable_sections = [
        (stations[start_idx], stations[end_idx])
        for start_idx, end_idx, _ in graph_edges
        if not mst.has_edge(start_idx, end_idx)
    ]

    return closable_sections, mst

if __name__ == "__main__":
    file_path = 'London Underground Data.xlsx'

    cleaned_data = load_underground_data(file_path)
    station_graph, graph_edges, stations = create_station_graph(cleaned_data)

    closable_routes, mst = find_closable_line_sections(station_graph, graph_edges, stations)

    print("Line Sections That Can Be Closed:")
    for start, end in closable_routes:
        print(f"{start} - {end}")

    print("\nMinimum Spanning Tree (MST) Edges:")
    print_undirected_edges(mst, stations)
    mst_weight = get_total_weight(mst)
    print(f"\nTotal Journey Time of MST: {mst_weight}")
