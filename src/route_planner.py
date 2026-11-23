
import json
from pathlib import Path

from alternative_routes import load_graph, find_alternative_routes, save_candidate_routes
from route_metrics import calculate_route_metrics
from check_transfer_feasibility import (
    load_train_stops,
    check_route_feasibility
)


# Locate project directory
BASE_DIR = Path(__file__).resolve().parent.parent

CANDIDATE_FILE = BASE_DIR / "data" / "processed" / "candidate_routes.json"

FEASIBLE_FILE = BASE_DIR / "feasible_candidate_routes.json"

CHECKED_FILE = BASE_DIR / "data" / "processed" / "checked_candidate_routes.json"


def main():

    print("\n========== TRAIN ROUTE PLANNER ==========")

    # STEP 1: Load railway graph
    print("\nLoading railway graph...")

    graph = load_graph()

    print("Railway graph loaded successfully.")

    # STEP 2: Take user input
    source = input("\nEnter source station code: ").strip().upper()

    destination = input("Enter destination station code: ").strip().upper()

    # STEP 3: Validate stations
    all_stations = set(graph.keys())

    for edges in graph.values():
        for edge in edges:
            all_stations.add(edge["destination"])

    if source not in all_stations:
        print("\nInvalid source station.")
        return

    if destination not in all_stations:
        print("\nInvalid destination station.")
        return

    if source == destination:
        print("\nSource and destination cannot be the same.")
        return

    # STEP 4: Generate alternative routes
    print("\nGenerating alternative routes...")

    routes = find_alternative_routes(
        graph,
        source,
        destination,
        max_routes=3
    )

    if not routes:
        print("\nNo routes found.")
        return

    print("Routes generated:", len(routes))

    # STEP 5: Calculate route metrics and save candidates
    print("\nCalculating route metrics...")

    save_candidate_routes(routes, source, destination)

    # STEP 6: Load candidate routes
    with open(CANDIDATE_FILE, "r", encoding="utf-8") as file:
        candidates = json.load(file)

    # STEP 7: Load train timetable
    print("\nLoading train timetable...")

    df = load_train_stops()

    print("Train timetable loaded successfully.")

    # STEP 8: Check transfer feasibility
    print("\nChecking transfer feasibility...")

    feasible_routes = []

    for route in candidates:

        checked_route = check_route_feasibility(route, df)

        route_id = checked_route["route_id"]

        print("\nRoute:", route_id)

        # Display route metrics
        metrics = checked_route["metrics"]

        print("Total distance:", metrics["total_distance"], "km")
        print("Connections:", metrics["connections"])
        print("Train changes:", metrics["train_changes"])
        print("Trains used:", metrics["trains_used"])

        # Display transfer results
        for transfer in checked_route["transfer_checks"]:

            print("\nInterchange station:", transfer["station"])

            print("Arrival:", transfer.get("arrival_time"))
            print("Departure:", transfer.get("departure_time"))

            print("Waiting time:", transfer.get("waiting_time"), "minutes")

            print("Transfer status:", transfer["is_feasible"])
        if checked_route["is_feasible"]:

            print("\nStatus: FEASIBLE")

            feasible_routes.append(checked_route)

        else:

            print("\nStatus: NOT FEASIBLE")

        print("-" * 50)

    # STEP 9: Save all checked routes
    with open(CHECKED_FILE, "w", encoding="utf-8") as file:
        json.dump(candidates, file, indent=4)

    # STEP 10: Save only feasible routes
    with open(FEASIBLE_FILE, "w", encoding="utf-8") as file:
        json.dump(feasible_routes, file, indent=4)

    # STEP 11: Final summary
    print("\n========== FINAL SUMMARY ==========")

    print("Total candidate routes:", len(candidates))

    print("Feasible routes:", len(feasible_routes))

    print("Infeasible routes:", len(candidates) - len(feasible_routes))

    print("\nAll checked routes saved to:", CHECKED_FILE)

    print("Feasible routes saved to:", FEASIBLE_FILE)

    print("\nRoute planning completed successfully!")


if __name__ == "__main__":
    main()
