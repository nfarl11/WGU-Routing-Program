import os
from datetime import datetime
from data_loader import load_distances, load_packages
from distance_matrix import build_address_dict
from routing import start_truck_route
from truck import Truck

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PACKAGE_PATH = os.path.join(BASE, "data", "fresh_package_file.csv")
DISTANCE_PATH = os.path.join(BASE, "data", "fresh_distance_table.csv")

def test_start_routing():
    # Load package and distance data
    package_table = load_packages(PACKAGE_PATH)

    locations, distance_matrix = load_distances(DISTANCE_PATH)
    matrix_index = {loc: i for i, loc in enumerate(locations)}

    # Create trucks
    t1 = Truck("Truck 1", datetime.strptime("08:00 AM", "%I:%M %p"))
    t2 = Truck("Truck 2", datetime.strptime("08:00 AM", "%I:%M %p"))
    t3 = Truck("Truck 3", datetime.strptime("10:20 AM", "%I:%M %p"))

    # Assign packages (same as main)
    t1.packages = [1, 2, 13, 14, 16, 15, 19, 39, 33, 34, 20, 21, 27, 35, 4, 40]
    t2.packages = [3, 18, 36, 38, 37, 5, 7, 29, 24, 23, 10, 22]
    t3.packages = [6, 9, 25, 28, 32, 26, 8, 30, 21, 17, 11, 31]

    trucks = [t1, t2, t3]

    print("Running full routing test...")
    total_miles = start_truck_route(
        trucks,
        package_table,
        matrix_index,
        distance_matrix
    )

    print("Total mileage:", total_miles)

    assert total_miles > 0, "Routing failed—total mileage never increased"

if __name__ == "__main__":
    test_start_routing()
