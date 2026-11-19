
import csv
from pathlib import Path
from collections import defaultdict

# Locate the project folder
project_folder = Path(__file__).resolve().parent.parent

# Locate the original timetable
file_path = project_folder / "data" / "raw" / "railway_timetable.csv"

with open(file_path, "r", encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)
    records = list(reader)

# 1. Find records with missing station names
print("\n===== MISSING STATION NAMES =====")

for row in records:
    if row["station_name"].strip() == "":     #checks if the station name is empty
        print(row)

# 2. Check whether one station code has multiple names
print("\n===== STATION CODE CHECK =====")

station_names = defaultdict(set)

for row in records:
    station_names[row["station_code"]].add(row["station_name"].strip())   #adding station names to the set for each station code

for code, names in station_names.items():   #code:dictionary key , names:dictionary value
    if len(names) > 1:
        print(code, ":", names)

# 3. Check whether one train number has multiple names
print("\n===== TRAIN NUMBER CHECK =====")

train_names = defaultdict(set)    #key:train number and value:set of train names associated with the number

for row in records:
    train_names[row["trainNumber"]].add(row["trainName"].strip())

for number, names in train_names.items():  
    if len(names) > 1:
        print(number, ":", names)
