from datetime import datetime

from address_to_location import address_to_location_dict
from data_loader import load_distances, load_packages
from distance_matrix import build_address_dict
from routing import start_truck_route
from truck import Truck

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

    for p_id in range(1, 41):
        pkg = package_table.lookup(str(p_id))

        if pkg.time_of_delivery is None:
            status = "At the hub"
        else:
            if pkg.time_of_delivery <= requested_time:
                status = f"Delivered at {pkg.time_of_delivery.strftime('%I:%M %p')}"
            else:
                status = "En route"

        print(f"Package {p_id}: {status}")


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
                print(f"Delivery time: {pkg.time_of_delivery.strftime('%I:%M %p')}\n")

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
    truck2 = Truck("Truck 2", datetime.strptime("09:05 AM", "%I:%M %p"))
    truck3 = Truck("Truck 3", datetime.strptime("10:20 AM", "%I:%M %p"))
    truck1.packages = [
        1,2,4,13,14,15,16,19,20,21,27,33,34,35,39,40,]  # 16
    truck2.packages = [
        3, 5, 6, 7, 10, 18, 22, 23, 24, 29, 30, 31, 36, 37, 38]  # 16
    truck3.packages = [
        8, 9, 11, 12, 17, 21, 25, 26, 28, 32]  # 9
    trucks = [truck1, truck2, truck3]
    total_mileage = 0
    for truck in trucks:
        mileage = start_truck_route(
            truck, package_table, index_map, distance_matrix, address_to_location_dict
        )
        total_mileage += mileage

    menu(package_table, total_mileage)