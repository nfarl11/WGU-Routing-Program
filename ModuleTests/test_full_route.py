import os
from datetime import datetime
import address_to_location
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
    matrix_index = build_address_dict(locations)
    address_to_location_dict = address_to_location.address_to_location_dict

    # Create trucks
    t1 = Truck("Truck 1", datetime.strptime("08:00 AM", "%I:%M %p"))
    t2 = Truck("Truck 2", datetime.strptime("09:05 AM", "%I:%M %p"))
    t3 = Truck("Truck 3", datetime.strptime("10:20 AM", "%I:%M %p"))

    # Assign packages (same as main)
    t1.packages = [
        1,
        2,
        4,
        13,
        14,
        15,
        16,
        19,
        20,
        27,
        33,
        34,
        35,
        39,
        40,
    ]  # 16
    t2.packages = [3, 5, 6, 7, 10, 18, 22, 23, 24, 29, 30, 31, 36, 37, 38]  # 16
    t3.packages = [8, 9, 11, 12, 17, 21, 25, 26, 28, 32]  # 9

    trucks = [t1, t2, t3]

    for truck in trucks:

        print("Running full routing test...")
        total_miles, current_time = start_truck_route(
            truck,
            package_table,
            matrix_index,
            distance_matrix,
            address_to_location_dict,
        )

        print(truck)

        assert total_miles > 0, "Routing failed—total mileage never increased"


if __name__ == "__main__":
    test_start_routing()
