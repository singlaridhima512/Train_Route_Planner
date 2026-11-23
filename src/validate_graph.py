
import json
import csv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "processed"

# Load railway graph
with open(DATA_DIR / "railway_graph.json", encoding="utf-8") as file:
    graph = json.load(file)

# Load station codes
with open(DATA_DIR / "stations.csv", encoding="utf-8-sig", newline="") as file:
    stations = {
        row["station_code"].strip().upper()
        for row in csv.DictReader(file)
    }

# Collect all graph nodes and connections
graph_nodes = set(graph.keys())
destinations = set()
total_edges = 0

for source, edges in graph.items():
    for edge in edges:
        total_edges += 1
        destinations.add(edge["destination"])

all_graph_stations = graph_nodes | destinations

# Validate graph
print("\n========== GRAPH VALIDATION ==========")

print("Total stations in stations.csv:", len(stations))
print("Total graph nodes:", len(graph_nodes))
print("Total unique stations in graph:", len(all_graph_stations))
print("Total connections:", total_edges)

print("\nStations missing from graph:")
print(sorted(stations - all_graph_stations))

print("\nUnknown stations in graph:")
print(sorted(all_graph_stations - stations))

# Check edge information
invalid_edges = []

for source, edges in graph.items():
    for edge in edges:
        if not edge.get("destination") or not edge.get("train_no"):
            invalid_edges.append((source, edge))

print("\nInvalid edges:", len(invalid_edges))
