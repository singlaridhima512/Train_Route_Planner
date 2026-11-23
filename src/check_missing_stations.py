
import csv
import json
from pathlib import Path
from collections import defaultdict

# Locate project files
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "processed"

# Load all station codes
with open(DATA_DIR / "stations.csv", encoding="utf-8-sig", newline="") as file:
    stations = {
        row["station_code"].strip().upper()
        for row in csv.DictReader(file)
    }

# Load graph
with open(DATA_DIR / "railway_graph.json", encoding="utf-8") as file:
    graph = json.load(file)

# Find stations missing from graph
missing = sorted(stations - set(graph))

# Load train stops and group them by train
trains = defaultdict(list)

with open(DATA_DIR / "train_stops.csv", encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        row["sequence"] = int(row["sequence"])
        trains[row["train_no"]].append(row)

# Sort every train's stops
for train_no in trains:
    trains[train_no].sort(key=lambda x: x["sequence"])

print("\n========== MISSING STATION ANALYSIS ==========")

for station in missing:

    print(f"\nStation: {station}")

    found = False

    for train_no, stops in trains.items():

        for i, stop in enumerate(stops):

            if stop["station_code"].strip().upper() == station:

                found = True

                previous = stops[i - 1]["station_code"] if i > 0 else "None"
                next_station = stops[i + 1]["station_code"] if i < len(stops) - 1 else "None"

                print("Train:", train_no)
                print("Sequence:", stop["sequence"])
                print("Previous station:", previous)
                print("Next station:", next_station)

    if not found:
        print("No valid train-stop record found for this station.")
