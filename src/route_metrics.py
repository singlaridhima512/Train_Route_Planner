
def calculate_route_metrics(route):

    if not route:
        return {
            "total_distance": 0,
            "connections": 0,
            "train_changes": 0,
            "trains_used": []
        }

    total_distance = 0
    trains_used = []

    for segment in route:

        edge = segment["edge"]

        # Calculate total distance
        distance = edge.get("distance")

        if distance is not None:
            total_distance += float(distance)

        # Collect train numbers in journey order
        train_no = edge["train_no"]

        if not trains_used or trains_used[-1] != train_no:
            trains_used.append(train_no)

    # Number of changes = number of distinct consecutive train groups - 1
    train_changes = max(0, len(trains_used) - 1)

    return {
        "total_distance": total_distance,
        "connections": len(route),
        "train_changes": train_changes,
        "trains_used": trains_used
    }
