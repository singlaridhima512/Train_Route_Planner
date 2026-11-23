
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

FILE = BASE_DIR / "data" / "processed" / "candidate_routes.json"

with open(FILE, "r", encoding="utf-8") as file:
    routes = json.load(file)

print("========== CANDIDATE ROUTES VALIDATION ==========")

print("Total candidate routes:", len(routes))

for route in routes:

    print("\nRoute ID:", route["route_id"])
    print("Source:", route["source"])
    print("Destination:", route["destination"])

    print("Connections:", route["metrics"]["connections"])
    print("Distance:", route["metrics"]["total_distance"])
    print("Train changes:", route["metrics"]["train_changes"])
    print("Trains:", route["metrics"]["trains_used"])

    print("Segments:", len(route["segments"]))

    assert len(route["segments"]) == route["metrics"]["connections"]

print("\nCandidate routes JSON verified successfully!")
