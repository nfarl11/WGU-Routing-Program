from datetime import datetime

import address_to_location
from address_to_location import address_to_location_dict
from data_loader import load_distances, load_packages
from distance_matrix import build_address_dict
from routing import get_nearest_neighbor
from truck import Truck

# Load in our package file, distance file and location dictionary

def start_routing(truck_array, package_table, matrix_index, distance_matrix, address_to_location_dict):

    active = True

    while active:
        active = False

        for truck in truck_array:

            if len(truck.packages) == 0:
                continue

            active = True

            next_loc, distance, package_id = get_nearest_neighbor(
                truck,
                package_table,
                matrix_index,
                distance_matrix,
                address_to_location_dict
            )

            pkg = package_table.lookup(str(package_id))

            truck.drive_to(next_loc, distance)
            truck.package_deliver(pkg)
            truck.packages.remove(package_id)

    # RETURN TOTAL MILES ACROSS ALL TRUCKS
    return sum(t.total_mileage for t in truck_array)

def parse_time_input(user_input):
    try:
        # Normalize ALL whitespace and capitalization
        cleaned = " ".join(user_input.split()).upper()
        return datetime.strptime(cleaned, "%I:%M %p")
    except ValueError:
        print("Invalid time format. Use HH:MM AM/PM (e.g., 12:20 PM).")
        return None

def print_status(package_table, requested_time):
    print(f"Status of package at {requested_time}:")

    for p_id in range (1,41):
        pkg = package_table.lookup(str(p_id))

        if pkg.time_of_delivery is None:
            status = "At the hub"
        else:
            delivered = datetime.strptime(pkg.delivery_time, "%I:%M %p")
            if delivered <= requested_time:
                status = f"Package delivered at {pkg.delivery_time,}"
            else:
                status = "En route"

        print(f"Package {p_id} delivered at {pkg.time_of_delivery,}: {status}")

def menu(package_table, total_miles):
    while True:
        print("\n--- WGUPS DELIVERY SYSTEM ---")
        print("1. Look up a package by ID")
        print("2. View all package statuses at a given time")
        print("3. Show total mileage")
        print("4. Exit")

        choice = input("\nEnter choice: ")

        if choice == "1":
            pid = input("Enter package ID: ")
            pkg = package_table.lookup(pid)

            if pkg is None:
                print("Invalid package ID.\n")
            else:
                print("\nPACKAGE INFO:")
                print(f"ID: {pkg.package_id}")
                print(f"Address: {pkg.package_address}")
                print(f"Deadline: {pkg.package_deadline}")
                print(f"Weight: {pkg.package_weight}")
                print(f"Status: {pkg.delivery_status}")
                print(f"Delivery time: {pkg.delivery_time}\n")

        elif choice == "2":
            t = input("Enter time (HH:MM AM/PM): ")
            query = parse_time_input(t)
            if query:
                print_status(package_table, query)

        elif choice == "3":
            print(f"\nTOTAL MILEAGE: {total_miles:.2f} miles\n")

        elif choice == "4":
            print("Exiting WGUPS system.\n")
            break

        else:
            print("Invalid choice.\n")

if __name__ == "__main__":
    package_table = load_packages("data/fresh_package_file.csv")
    locations, distance_matrix = load_distances("data/fresh_distance_table.csv")
    index_map = build_address_dict(locations)
    start_time = datetime.strptime("08:00 AM", "%I:%M %p")
    truck1 = Truck("Truck 1", start_time)
    truck2 = Truck("Truck 2", start_time)
    truck3 = Truck("Truck 3", datetime.strptime("10:20 AM", "%I:%M %p"))
    truck1.packages = [1, 2, 13, 14, 16, 15, 19, 39, 33, 34, 20, 21, 27, 35, 4, 40]
    truck2.packages = [3, 18, 36, 38, 37, 5, 7, 29, 24, 23, 10, 22]
    truck3.packages = [6, 9, 25, 28, 32, 26, 8, 30, 21, 17, 11, 31]
    trucks = [truck1, truck2, truck3]

    total_mileage = start_routing(trucks,package_table,index_map,distance_matrix,address_to_location_dict)

    menu(package_table, total_mileage)

'''
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
    nearest_loc, dist, pid = get_nearest_neighbor(
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
    print("Package ID:",pid)
    print("\nExpected:")
    if urgent:
        print(" ➤ Because urgent packages exist, chosen location should belong to an urgent package.")
        print(" ➤ EXCEPT if an EOD package is closer (your EOD optimization).")
    else:
        print(" ➤ No urgent packages left → normal nearest neighbor should be applied.")


if __name__ == "__main__":
    debug_test_nearest_neighbor(truck1)
'''