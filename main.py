from datetime import datetime
from data_loader import load_distances, load_packages
from distance_matrix import build_address_dict
from truck import Truck

# Load in our package file, distance file and location dictionary
package_table = load_packages("data/fresh_package_file.csv")
locations, distance_matrix = load_distances("data/fresh_distance_table.csv")
address_to_location = build_address_dict(locations)

start_time = datetime.strptime("08:00 AM", "%I:%M %p")
truck1 = Truck("Truck 1", start_time)
truck2 = Truck("Truck 2", start_time)
truck3 = Truck("Truck 3", start_time)
truck1_packages = [
    1,
    2,
    13,
    16,
    15,
    19,
]
truck2_packages = [3, 18, 36, 38]
truck3_packages = [
    6,
    9,
    25,
    28,
    32,
]
