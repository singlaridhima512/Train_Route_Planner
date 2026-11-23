
import csv
from pathlib import Path

# STEP 1: Locate project folders
project_folder = Path(__file__).resolve().parent.parent

input_file = project_folder / "data" / "raw" / "railway_timetable.csv"
output_folder = project_folder / "data" / "processed"

# STEP 2: Create processed folder if it doesn't exist
output_folder.mkdir(parents=True, exist_ok=True)

# STEP 3: Prepare dictionaries to store unique data
trains = {}
stations = {}
train_stops = []

# STEP 4: Read the original railway timetable
with open(input_file, "r", encoding="utf-8-sig", newline="") as file:

    reader = csv.DictReader(file)

    for row in reader:

        train_no = row["trainNumber"].strip()
        train_name = row["trainName"].strip()
        station_code = row["station_code"].strip()
        station_name = row["station_name"].strip()
        sequence = row["stnSerialNumber"].strip()

        # Skip rows missing essential information
        if not train_no or not station_code or not sequence:
            continue

        # Store unique train details
        if train_no not in trains:
            trains[train_no] = {
                "train_no": train_no,
                "train_name": train_name
            }

        # Store unique station details
        if station_code not in stations:
            stations[station_code] = {
                "station_code": station_code,
                "station_name": station_name
            }
        elif not stations[station_code]["station_name"] and station_name:
            #checks if station already exist
            #stored name is empty
            #current row contains  a station name
            stations[station_code]["station_name"] = station_name

        # Store every train stop
        train_stops.append({
            "train_no": train_no,
            "sequence": sequence,
            "station_code": station_code,
            "station_name": station_name,
            "distance": row["distance"].strip(),
            "arrival": row["arrivalTime"].strip(),
            "departure": row["departureTime"].strip()
        })


# STEP 5: Sort train stops by train number and sequence
train_stops.sort(
    key=lambda stop: (stop["train_no"], int(stop["sequence"]))   #lambda is an anonymous function that takes on stop record nd return train number and converts seq number into integer
)


# STEP 6: Function to save data into CSV files
def save_csv(filename, data, columns):

    output_file = output_folder / filename

    with open(output_file, "w", encoding="utf-8", newline="") as file:

        writer = csv.DictWriter(file, fieldnames=columns) #writes dictionary records into a CSV file.

        writer.writeheader()  #writes the column names into the first row of the CSV file.
        writer.writerows(data)  #writes all the dictionaries as rows in the CSV.

    print(f"{filename} created successfully!")


# STEP 7: Generate three processed CSV files

save_csv(
    "trains.csv",
    list(trains.values()),
    ["train_no", "train_name"]
)

save_csv(
    "stations.csv",
    list(stations.values()),
    ["station_code", "station_name"]
)

save_csv(
    "train_stops.csv",
    train_stops,
    [
        "train_no",
        "sequence",
        "station_code",
        "station_name",
        "distance",
        "arrival",
        "departure"
    ]
)


# STEP 8: Display preprocessing summary
print("\n========== PREPROCESSING SUMMARY ==========")

print("Total unique trains:", len(trains))
print("Total unique stations:", len(stations))
print("Total train stops:", len(train_stops))

print("\nPreprocessing completed successfully!")
