from route_metrics import calculate_route_metrics
import json
from pathlib import Path
from collections import deque

BASE_DIR = Path(__file__).resolve().parent.parent
GRAPH_FILE = BASE_DIR / "data" / "processed" / "railway_graph.json"


def load_graph():
    with open(GRAPH_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def bfs_alternative(graph, source, destination, blocked_edges):
    queue = deque([(source, [])])
    visited = {source}

    while queue:
        current, path = queue.popleft()

        if current == destination:
            return path

        for edge in graph.get(current, []):

            next_station = edge["destination"]

            edge_id = (current, next_station, edge["train_no"])

            if edge_id in blocked_edges:
                continue

            if next_station not in visited:
                visited.add(next_station)

                new_path = path + [{
                    "source": current,
                    "destination": next_station,
                    "edge": edge
                }]

                queue.append((next_station, new_path))

    return None


def find_alternative_routes(graph, source, destination, max_routes=3):

    routes = []
    blocked_edges = set()

    for _ in range(max_routes):

        route = bfs_alternative(
            graph,
            source,
            destination,
            blocked_edges
        )

        if route is None:
            break

        routes.append(route)

        # Block one edge from the newly found route
        if route:
            middle_index = len(route) // 2

            segment = route[middle_index]

            blocked_edges.add((
                segment["source"],
                segment["destination"],
                segment["edge"]["train_no"]
            ))

    return routes


def save_candidate_routes(routes, source, destination):

    output_file = (
        BASE_DIR / "data" / "processed" / "candidate_routes.json"
    )

    candidate_data = []

    for index, route in enumerate(routes, start=1):

        metrics = calculate_route_metrics(route)

        candidate = {
            "route_id": index,
            "source": source,
            "destination": destination,
            "segments": route,
            "metrics": metrics
        }

        candidate_data.append(candidate)

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(candidate_data, file, indent=4)

    print("\nCandidate routes saved successfully!")
    print("Output file:", output_file)



def main():

    graph = load_graph()

    source = input("Enter source station code: ").strip().upper()
    destination = input("Enter destination station code: ").strip().upper()

    all_stations = set(graph.keys())

    for edges in graph.values():
        for edge in edges:
            all_stations.add(edge["destination"])

    if source not in all_stations:
        print("Invalid source station.")
        return

    if destination not in all_stations:
        print("Invalid destination station.")
        return

    routes = find_alternative_routes(
        graph,
        source,
        destination,
        max_routes=3
    )

    save_candidate_routes(routes, source, destination)

    print("\n========== ALTERNATIVE ROUTES ==========")

    if not routes:
        print("No route found.")
        return

    for i, route in enumerate(routes, start=1):

        print(f"\nRoute {i}")
        print("Connections:", len(route))
        metrics = calculate_route_metrics(route)

        print("Total distance:", metrics["total_distance"], "km")
        print("Train changes:", metrics["train_changes"])
        print("Trains used:", metrics["trains_used"])

        for segment in route:
            print(
                segment["source"],
                "->",
                segment["destination"],
                "| Train:",
                segment["edge"]["train_no"]
            )


if __name__ == "__main__":
    main()

