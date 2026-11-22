
"""
Route metrics for the Train Route Planner optimization module.

Temporary route format:
{
    "legs": [
        {
            "train_id": "T101",
            "travel_time_minutes": 60,
            "distance_km": 40
        }
    ]
}
"""


def _get_legs(route):
    """Extract and validate the list of legs from a route."""
    if not isinstance(route, dict):
        raise TypeError("Route must be a dictionary.")

    legs = route.get("legs")

    if not isinstance(legs, list):
        raise ValueError("Route must contain a 'legs' list.")

    return legs


def total_travel_time(route):
    """Return total travel time in minutes."""
    legs = _get_legs(route)

    total = 0

    for leg in legs:
        time = leg.get("travel_time_minutes", 0)

        if not isinstance(time, (int, float)) or time < 0:
            raise ValueError("Travel time must be a non-negative number.")

        total += time

    return total


def total_distance(route):
    """Return total distance in kilometers."""
    legs = _get_legs(route)

    total = 0

    for leg in legs:
        distance = leg.get("distance_km", 0)

        if not isinstance(distance, (int, float)) or distance < 0:
            raise ValueError("Distance must be a non-negative number.")

        total += distance

    return total


def count_transfers(route):
    """Count train changes between consecutive route legs."""
    legs = _get_legs(route)

    transfers = 0

    for i in range(1, len(legs)):
        previous_train = legs[i - 1].get("train_id")
        current_train = legs[i].get("train_id")

        if previous_train != current_train:
            transfers += 1

    return transfers


def route_metrics(route):
    """Return all route metrics together."""
    legs = _get_legs(route)

    return {
        "total_travel_time": total_travel_time(route),
        "total_distance": total_distance(route),
        "count_transfers": count_transfers(route),
        "number_of_legs": len(legs),
    }
