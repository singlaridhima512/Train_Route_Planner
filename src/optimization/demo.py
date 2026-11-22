
"""Demo program for the Train Route Planner optimization package."""

from src.optimization import route_metrics, rank_routes


def main():
    # Sample routes for testing the optimization package.
    routes = [
        {
            "route_id": "Route A",
            "legs": [
                {
                    "train_id": "T101",
                    "travel_time_minutes": 120,
                    "distance_km": 100,
                }
            ],
        },
        {
            "route_id": "Route B",
            "legs": [
                {
                    "train_id": "T102",
                    "travel_time_minutes": 60,
                    "distance_km": 80,
                }
            ],
        },
        {
            "route_id": "Route C",
            "legs": [
                {
                    "train_id": "T103",
                    "travel_time_minutes": 75,
                    "distance_km": 50,
                },
                {
                    "train_id": "T104",
                    "travel_time_minutes": 30,
                    "distance_km": 20,
                },
            ],
        },
    ]

    print("TRAIN ROUTE PLANNER - OPTIMIZATION DEMO")
    print("=" * 45)

    # Calculate metrics for each route.
    for route in routes:
        metrics = route_metrics(route)

        print(f"\n{route['route_id']}")
        print(f"Travel time: {metrics['total_travel_time']} minutes")
        print(f"Distance: {metrics['total_distance']} km")
        print(f"Transfers: {metrics['count_transfers']}")

    # Rank routes from best to worst.
    ranked_routes = rank_routes(routes)

    print("\nROUTE RANKING")
    print("=" * 45)

    for position, result in enumerate(ranked_routes, start=1):
        route = result["route"]
        metrics = result["metrics"]

        print(f"\nRank {position}: {route['route_id']}")
        print(f"Score: {result['score']}")
        print(f"Travel time: {metrics['total_travel_time']} minutes")
        print(f"Distance: {metrics['total_distance']} km")
        print(f"Transfers: {metrics['count_transfers']}")


if __name__ == "__main__":
    main()
