
import pandas as pd
import json
from pathlib import Path
from datetime import datetime


# ---------------- PATHS AND SETTINGS ----------------

BASE_DIR = Path(__file__).resolve().parent.parent

TRAIN_STOPS_FILE = BASE_DIR / "data" / "processed" / "train_stops.csv"
CANDIDATE_ROUTES_FILE = BASE_DIR / "data" / "processed" / "candidate_routes.json"

CHECKED_OUTPUT_FILE = BASE_DIR / "data" / "processed" / "checked_candidate_routes.json"
FEASIBLE_OUTPUT_FILE = BASE_DIR / "feasible_candidate_routes.json"

MIN_TRANSFER_TIME = 30


# ---------------- NORMALIZATION ----------------

def normalize_train_no(train_no):
    return str(train_no).strip().lstrip("0") or "0"


def normalize_station_code(station_code):
    return str(station_code).strip().upper()


# ---------------- LOAD TRAIN TIMETABLE ----------------

def load_train_stops():

    df = pd.read_csv(TRAIN_STOPS_FILE, dtype=str)

    df["train_no"] = df["train_no"].apply(normalize_train_no)
    df["station_code"] = df["station_code"].apply(normalize_station_code)

    return df


# ---------------- GET TRAIN TIMING ----------------

def get_station_timing(df, train_no, station_code, timing_type):

    train_no = normalize_train_no(train_no)
    station_code = normalize_station_code(station_code)

    records = df[
        (df["train_no"] == train_no) &
        (df["station_code"] == station_code)
    ]

    if records.empty:
        return None

    return records.iloc[0][timing_type]


# ---------------- CONVERT TIME INTO MINUTES ----------------

def time_to_minutes(time_value):

    if pd.isna(time_value) or not str(time_value).strip():
        return None

    time_value = str(time_value).strip().upper()

    formats = [
        "%I:%M %p",
        "%H:%M",
        "%H:%M:%S"
    ]

    for time_format in formats:
        try:
            parsed_time = datetime.strptime(time_value, time_format)
            return parsed_time.hour * 60 + parsed_time.minute
        except ValueError:
            continue

    return None


# ---------------- CHECK ONE TRANSFER ----------------

def check_transfer(df, incoming_train, outgoing_train, station_code):

    incoming_train = normalize_train_no(incoming_train)
    outgoing_train = normalize_train_no(outgoing_train)
    station_code = normalize_station_code(station_code)

    arrival = get_station_timing(
        df, incoming_train, station_code, "arrival"
    )

    departure = get_station_timing(
        df, outgoing_train, station_code, "departure"
    )

    arrival_minutes = time_to_minutes(arrival)
    departure_minutes = time_to_minutes(departure)

    result = {
        "station": station_code,
        "incoming_train": incoming_train,
        "outgoing_train": outgoing_train,
        "arrival": arrival,
        "departure": departure,
        "waiting_time": None,
        "is_feasible": False,
        "reason": ""
    }

    if arrival_minutes is None:
        result["reason"] = "Incoming train arrival time not found"
        return result

    if departure_minutes is None:
        result["reason"] = "Outgoing train departure time not found"
        return result

    # If departure clock time is earlier, assume it is on the next day.
    if departure_minutes < arrival_minutes:
        departure_minutes += 24 * 60

    waiting_time = departure_minutes - arrival_minutes

    result["waiting_time"] = waiting_time
    result["is_feasible"] = waiting_time >= MIN_TRANSFER_TIME

    if result["is_feasible"]:
        result["reason"] = "Sufficient transfer time"
    else:
        result["reason"] = "Insufficient transfer time"

    return result


# ---------------- CHECK COMPLETE ROUTE ----------------

def check_route_feasibility(route, df):

    segments = route.get("segments", [])
    transfer_checks = []

    for i in range(len(segments) - 1):

        current_segment = segments[i]
        next_segment = segments[i + 1]

        incoming_train = current_segment["edge"]["train_no"]
        outgoing_train = next_segment["edge"]["train_no"]

        # No transfer is required if both segments use the same train.
        if normalize_train_no(incoming_train) == normalize_train_no(outgoing_train):
            continue

        interchange_station = current_segment["destination"]

        transfer_result = check_transfer(
            df,
            incoming_train,
            outgoing_train,
            interchange_station
        )

        transfer_checks.append(transfer_result)

    route["transfer_checks"] = transfer_checks

    route["is_feasible"] = all(
        check["is_feasible"] for check in transfer_checks
    )

    return route


# ---------------- MAIN PROGRAM ----------------

def main():

    print("\n========== TRANSFER FEASIBILITY CHECK ==========\n")

    print("Loading train timetable...")

    df = load_train_stops()

    print("Train timetable loaded successfully!")

    print("\nLoading candidate routes...")

    with open(CANDIDATE_ROUTES_FILE, "r") as file:
        candidate_routes = json.load(file)

    print("Candidate routes loaded:", len(candidate_routes))

    checked_routes = []

    print("\nChecking transfer feasibility...\n")

    for route in candidate_routes:

        checked_route = check_route_feasibility(route, df)
        checked_routes.append(checked_route)

        print(f"Route: {checked_route.get('route_id')}")

        metrics = checked_route.get("metrics", {})

        print("Total distance:", metrics.get("total_distance"), "km")
        print("Connections:", metrics.get("connections"))
        print("Train changes:", metrics.get("train_changes"))
        print("Trains used:", metrics.get("trains_used"))

        if not checked_route["transfer_checks"]:
            print("No train changes required.")

        for transfer in checked_route["transfer_checks"]:

            print("\nInterchange station:", transfer["station"])
            print("Incoming train:", transfer["incoming_train"])
            print("Outgoing train:", transfer["outgoing_train"])
            print("Arrival:", transfer["arrival"])
            print("Departure:", transfer["departure"])
            print("Waiting time:", transfer["waiting_time"], "minutes")
            print("Reason:", transfer["reason"])
            print("Transfer status:", transfer["is_feasible"])

        print("\nStatus:", "FEASIBLE" if checked_route["is_feasible"] else "NOT FEASIBLE")
        print("-" * 50)

    # Save all checked routes.
    with open(CHECKED_OUTPUT_FILE, "w") as file:
        json.dump(checked_routes, file, indent=4)

    # Keep only feasible routes.
    feasible_routes = [
        route for route in checked_routes
        if route["is_feasible"]
    ]

    with open(FEASIBLE_OUTPUT_FILE, "w") as file:
        json.dump(feasible_routes, file, indent=4)

    # Final summary.
    print("\n========== FINAL SUMMARY ==========")

    print("Total candidate routes:", len(checked_routes))
    print("Feasible routes:", len(feasible_routes))
    print("Infeasible routes:", len(checked_routes) - len(feasible_routes))

    print("\nAll checked routes saved to:")
    print(CHECKED_OUTPUT_FILE)

    print("\nFeasible routes saved to:")
    print(FEASIBLE_OUTPUT_FILE)

    print("\nTransfer feasibility check completed!")


if __name__ == "__main__":
    main()
