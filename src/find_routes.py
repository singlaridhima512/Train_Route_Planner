
import json
from pathlib import Path
from collections import deque
import csv


# Locate project directory
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "processed"

GRAPH_FILE = DATA_DIR / "railway_graph.json"
TRAINS_FILE = DATA_DIR / "trains.csv"
STATIONS_FILE = DATA_DIR / "stations.csv"


# Load railway graph
def load_graph():

    with open(GRAPH_FILE, "r", encoding="utf-8") as file:
        graph = json.load(file)

    return graph


# Load station names
def load_stations():

    station_names = {}

    with open(STATIONS_FILE, "r", encoding="utf-8-sig", newline="") as file:

        reader = csv.DictReader(file)

        for row in reader:
            code = row["station_code"].strip().upper()
            name = row["station_name"].strip()

            station_names[code] = name

    return station_names


# Load train names
def load_trains():

    train_names = {}

    with open(TRAINS_FILE, "r", encoding="utf-8-sig", newline="") as file:

        reader = csv.DictReader(file)

        for row in reader:
            train_names[row["train_no"]] = row["train_name"]

    return train_names


# BFS route finding algorithm
def bfs(graph, source, destination):

    queue = deque([source])

    visited = set()
    visited.add(source)

    # Store the previous station and connection
    parent = {}

    while queue:

        current_station = queue.popleft()

        # Destination found
        if current_station == destination:
            break

        # Explore neighbouring stations
        for edge in graph.get(current_station, []):

            next_station = edge["destination"]

            if next_station not in visited:

                visited.add(next_station)

                parent[next_station] = {
                    "previous_station": current_station,
                    "edge": edge
                }

                queue.append(next_station)

    # No route found
    if destination not in visited:
        return None

    # Reconstruct route
    route = []
    current_station = destination

    while current_station != source:

        information = parent[current_station]

        route.append({
            "source": information["previous_station"],
            "destination": current_station,
            "edge": information["edge"]
        })

        current_station = information["previous_station"]

    route.reverse()

    return route


# Display route
def display_route(route, station_names, train_names):

    if route is None:
        print("\nNo route found between these stations.")
        return

    print("\n========== ROUTE DETAILS ==========")

    print("Number of connections:", len(route))

    print("\nJourney:")

    for segment in route:

        source = segment["source"]
        destination = segment["destination"]
        edge = segment["edge"]

        train_no = edge["train_no"]
        train_name = train_names.get(train_no, "Unknown Train")

        source_name = station_names.get(source, source)
        destination_name = station_names.get(destination, destination)

        print(f"\n{source_name} ({source}) -> {destination_name} ({destination})")

        print("Train:", train_no, "-", train_name)
        print("Distance:", edge["distance"], "km")
        print("Departure:", edge["departure"])
        print("Arrival:", edge["arrival"])


# Main program
if __name__ == "__main__":

    graph = load_graph()
    station_names = load_stations()
    train_names = load_trains()

    print("========== RAILWAY ROUTE PLANNER ==========")

    source = input("Enter source station code: ").strip().upper()
    destination = input("Enter destination station code: ").strip().upper()

    # Check whether stations exist in the dataset
    all_stations = set(graph.keys())

    for edges in graph.values():
        for edge in edges:
            all_stations.add(edge["destination"])

    if source not in all_stations:
        print("Invalid source station code.")

    elif destination not in all_stations:
        print("Invalid destination station code.")

    else:

        route = bfs(graph, source, destination)

        display_route(route, station_names, train_names)
