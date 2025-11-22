from datetime import datetime
from data_loader import load_distances, load_packages
from distance_matrix import build_address_dict
from hash_table import HashTable
from routing import get_nearest_neighbor
from truck import Truck

# Load in our package file, distance file and location dictionary
package_table = load_packages("data/fresh_package_file.csv")
locations, distance_matrix = load_distances("data/fresh_distance_table.csv")
address_to_location = build_address_dict(locations)
print(address_to_location)

start_time = datetime.strptime("08:00 AM", "%I:%M %p")
truck1 = Truck("Truck 1", start_time)
truck2 = Truck("Truck 2", start_time)
truck3 = Truck("Truck 3", datetime.strptime("10:20 AM", "%I:%M %p"))
truck1_packages = [1, 2, 13, 14, 16, 15, 19, 39, 33, 34, 20, 21, 27, 35, 4, 40]
truck2_packages = [3, 18, 36, 38, 37, 5, 7, 29, 24, 23, 10, 22]
truck3_packages = [6, 9, 25, 28, 32, 26, 8, 30, 21, 17, 11, 31]
for package in truck1_packages:
    truck1.add_package(package)


def debug_test_nearest_neighbor(truck1):
    print(f"\n=== DEBUG: Testing nearest neighbor for {truck1.truck_number} ===")

    urgent = []
    eod = []

    # Inspect package deadlines
    for pid in truck1.packages:
        pkg = package_table.lookup(str(pid))
        print(f"  Package {pid} deadline = {pkg.package_deadline}")

        if pkg.delivery_status == "Delivered":
            continue

        if pkg.package_deadline != "EOD":
            urgent.append(pid)
        else:
            eod.append(pid)

    print("\nUrgent packages:", urgent)
    print("EOD packages:", eod)

    # Run your nearest neighbor function
    nearest_loc, dist = get_nearest_neighbor(
        truck1,
        package_table,
        address_to_location,
        distance_matrix,
    )

    print("\nChosen next location index:", nearest_loc)
    print("Distance to next stop:", dist)

    # reverse lookup location name
    loc_name = None
    for name, idx in address_to_location.items():
        if idx == nearest_loc:
            loc_name = name

    print("Location name:", loc_name)
    print("\nExpected:")
    if urgent:
        print(" ➤ Because urgent packages exist, chosen location should belong to an urgent package.")
        print(" ➤ EXCEPT if an EOD package is closer (your EOD optimization).")
    else:
        print(" ➤ No urgent packages left → normal nearest neighbor should be applied.")


if __name__ == "__main__":
    debug_test_nearest_neighbor(truck1)
