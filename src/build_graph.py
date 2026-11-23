
import csv
import json
from pathlib import Path
from collections import defaultdict


# --------------------------------------------------
# STEP 1: DEFINE FILE PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

TRAIN_STOPS_FILE = BASE_DIR / "data" / "processed" / "train_stops.csv"

OUTPUT_FILE = BASE_DIR / "data" / "processed" / "railway_graph.json"


# --------------------------------------------------
# STEP 2: LOAD TRAIN STOP DATA
# --------------------------------------------------

def load_train_stops():

    records = []

    with open(TRAIN_STOPS_FILE, "r", encoding="utf-8-sig", newline="") as file:

        reader = csv.DictReader(file)

        required_columns = {
            "train_no",
            "sequence",
            "station_code"
        }

        if not required_columns.issubset(reader.fieldnames or []):
            raise ValueError(
                f"Missing required columns: {required_columns - set(reader.fieldnames or [])}"
            )

        for row in reader:

            # Skip rows with missing essential information
            if not row["train_no"].strip() or not row["station_code"].strip():
                continue

            try:
                row["sequence"] = int(row["sequence"])
            except (ValueError, TypeError):
                continue

            # Clean station and train identifiers
            row["train_no"] = row["train_no"].strip()
            row["station_code"] = row["station_code"].strip().upper()

            records.append(row)

    print("Total valid train-stop records:", len(records))

    return records


# --------------------------------------------------
# STEP 3: GROUP STOPS BY TRAIN
# --------------------------------------------------

def group_stops_by_train(records):

    trains = defaultdict(list)

    for row in records:

        train_no = row["train_no"]

        trains[train_no].append(row)

    # Sort stations according to their sequence number
    for train_no in trains:

        trains[train_no].sort(
            key=lambda x: x["sequence"]
        )

    print("Total trains:", len(trains))

    return trains


# --------------------------------------------------
# STEP 4: BUILD THE RAILWAY GRAPH
# --------------------------------------------------

def build_graph(trains):

    graph = defaultdict(list)

    total_edges = 0

    for train_no, stops in trains.items():

        # Compare consecutive stations
        for i in range(len(stops) - 1):

            current_stop = stops[i]
            next_stop = stops[i + 1]

            source = current_stop["station_code"]
            destination = next_stop["station_code"]

            # Avoid invalid self-connections
            if source == destination:
                continue

            # Calculate distance between consecutive stations
            distance = None

            try:
                current_distance = float(current_stop["distance"])
                next_distance = float(next_stop["distance"])

                distance = next_distance - current_distance

                if distance < 0:
                    distance = None

            except (ValueError, TypeError, KeyError):
                pass

            # Store connection information
            edge = {
                "destination": destination,
                "train_no": train_no,
                "distance": distance,
                "departure": current_stop.get("departure", ""),
                "arrival": next_stop.get("arrival", ""),
                "source_sequence": current_stop["sequence"],
                "destination_sequence": next_stop["sequence"]
            }

            graph[source].append(edge)

            total_edges += 1

    print("Total stations in graph:", len(graph))
    print("Total connections in graph:", total_edges)

    return dict(graph)


# --------------------------------------------------
# STEP 5: SAVE GRAPH AS JSON
# --------------------------------------------------

def save_graph(graph):

    # Convert graph into a normal dictionary
    graph_data = dict(graph)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:

        json.dump(
            graph_data,
            file,
            indent=4
        )

    print("\nGraph successfully saved!")
    print("Output file:", OUTPUT_FILE)


# --------------------------------------------------
# STEP 6: DISPLAY GRAPH SUMMARY
# --------------------------------------------------

def display_graph_summary(graph):

    print("\n----- RAILWAY GRAPH SUMMARY -----")

    print("Number of stations:", len(graph))

    total_connections = sum(
        len(edges) for edges in graph.values()
    )

    print("Number of connections:", total_connections)

    print("\nSample connections:")

    count = 0

    for station, edges in graph.items():

        for edge in edges:

            print(
                station,
                "->",
                edge["destination"],
                "| Train:",
                edge["train_no"],
                "| Distance:",
                edge["distance"]
            )

            count += 1

            if count == 10:
                return


# --------------------------------------------------
# MAIN EXECUTION
# --------------------------------------------------

if __name__ == "__main__":

    records = load_train_stops()

    trains = group_stops_by_train(records)

    railway_graph = build_graph(trains)

    save_graph(railway_graph)

    display_graph_summary(railway_graph)
