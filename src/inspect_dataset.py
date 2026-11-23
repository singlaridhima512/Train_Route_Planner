#opens railway_timetable.csv   
#reads col names,counts total no. of records,displays first five rec,identifies info in dataset

import csv
from pathlib import Path

# STEP 1: Locate the project folder
project_folder = Path(__file__).resolve().parent.parent #parent takes one folder back(src to trainrouteplanner)

# STEP 2: Locate the railway timetable CSV file
file_path = project_folder / "data" / "raw" / "railway_timetable.csv"

# STEP 3: Check whether the file exists
if not file_path.exists():
    print("Error: Railway timetable file not found!")
else:

    # STEP 4: Open the CSV file
    with open(file_path, "r", encoding="utf-8-sig", newline="") as file:

        # STEP 5: Read the CSV data
        reader = csv.DictReader(file)    #DictReader reads each row as dictionary

        # STEP 6: Display column names
        print("\nCOLUMN NAMES:")
        print(reader.fieldnames)         #which columns are available in original dataset

        # STEP 7: Read the first five records
        print("\nFIRST FIVE RECORDS:")

        for i, row in enumerate(reader):    #enumerate gives index for every row
            if i == 5:
                break
            print(row)

