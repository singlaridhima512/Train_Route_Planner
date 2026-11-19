'''if a large no. of dataset
->how many col
->duplicates?
->missing values?
->train info col?
->station info col?
->what kind of values stored?
'''


import csv
from pathlib import Path
from collections import Counter

# STEP 1: Locate the project folder
project_folder = Path(__file__).resolve().parent.parent

# STEP 2: Locate the raw railway dataset
file_path = project_folder / "data" / "raw" / "railway_timetable.csv"

# STEP 3: Check whether the file exists
if not file_path.exists():
    print("Dataset not found!")

else:

    # STEP 4: Open and read the CSV file
    with open(file_path, "r", encoding="utf-8-sig", newline="") as file:

        reader = csv.DictReader(file)

        # STEP 5: Store column names
        columns = reader.fieldnames

        # STEP 6: Store all records
        records = list(reader)     #remaining csv records into a dictionary

    # STEP 7: Display basic dataset information
    print("\n========== DATASET OVERVIEW ==========")

    print("Total rows:", len(records))     #total no. of records
    print("Total columns:", len(columns))  #total no. of col
    print("Column names:", columns)

    # STEP 8: Count missing values
    print("\n========== MISSING VALUES ==========")

    for column in columns:

        missing_count = 0

        for row in records:

            value = row[column]

            if value is None or value.strip() == "":   #none means no value provided
                missing_count += 1

        print(column, ":", missing_count)

    # STEP 9: Count duplicate records
    print("\n========== DUPLICATE RECORDS ==========")

    unique_records = set()
    duplicate_count = 0

    for row in records:

        #converts dictionary into tuple bcz set cant directly store values of dictionary
        record_tuple = tuple(      
            (column, row[column]) for column in columns
        )

        if record_tuple in unique_records:
            duplicate_count += 1

        else:
            unique_records.add(record_tuple)

    print("Duplicate records:", duplicate_count)

    # STEP 10: Display unique values in each column
    print("\n========== UNIQUE VALUES ==========")

    for column in columns:

        values = set()

        for row in records:
            values.add(row[column])

        print(column, ":", len(values))

    # STEP 11: Display sample records
    print("\n========== SAMPLE RECORDS ==========")

    for row in records[:5]:     #first five elements from list
        print(row)
