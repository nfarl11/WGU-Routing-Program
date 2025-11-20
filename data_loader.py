import csv

def load_packages(path="data/fresh_package_file.csv"):
    packages = []
    with open(path, "r") as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for row in reader:
            if row:  # avoid blank lines
                packages.append(row)
    return packages


def load_distances(path="data/fresh_distance_table.csv"):
    matrix = []
    with open(path, "r") as f:
        reader = csv.reader(f)
        locations = next(reader)  # This reads the header row


        for row in reader:
            # Skip blank rows
            if not row or all(cell.strip() == "" for cell in row):
                continue

            # Convert ALL columns to float (no slicing)
            float_row = [float(x.strip()) for x in row]
            matrix.append(float_row)

    return locations, matrix
