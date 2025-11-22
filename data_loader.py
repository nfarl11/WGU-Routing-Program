import csv
import hash_table
import package


# Method for extracting package data from package csv, create hash table and insert
def load_packages(path="data/fresh_package_file.csv"):
    table = hash_table.HashTable()

    with open(path, "r") as f:
        reader = csv.reader(f)
        next(reader)  # skip first row of headers
        for row in reader:
            if not row or all(
                cell.strip() == "" for cell in row
            ):  # Clean cells for empty white space and skip if empty
                continue
            pack = package.Package(
                package_id=row[0],
                package_address=row[1],
                package_city=row[2],
                package_state=row[3],
                package_zip=row[4],
                package_deadline=row[5],
                package_weight=row[6],
            )

            table.insert(pack.package_id, pack)

    return table


# Method for extracting distance data from distance csv
def load_distances(path="data/fresh_distance_table.csv"):
    matrix = []
    with open(path, "r") as f:
        reader = csv.reader(f)
        locations = next(reader)  # This reads the header row

        for row in reader:
            if not row or all(
                cell.strip() == "" for cell in row
            ):  # Clean cells for empty white space and skip if empty
                continue

            float_row = [
                float(x.strip()) for x in row
            ]  # Convert ALL columns to float (no slicing)
            matrix.append(float_row)
    return locations, matrix

