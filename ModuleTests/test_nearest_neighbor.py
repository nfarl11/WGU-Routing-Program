import os
from data_loader import load_packages, load_distances
from routing import get_nearest_neighbor
from truck import Truck
from address_to_location import address_to_location_dict

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PACKAGE_PATH = os.path.join(BASE, "data", "fresh_package_file.csv")
DISTANCE_PATH = os.path.join(BASE, "data", "fresh_distance_table.csv")

def test_nn_for_one_truck():
    packages = load_packages(PACKAGE_PATH)
    locations, matrix = load_distances(DISTANCE_PATH)
    index_map = {loc: i for i, loc in enumerate(locations)}

    truck = Truck("Test", None)
    truck.packages = [1, 2, 3]

    loc, dist, pkg = get_nearest_neighbor(
        truck, packages, index_map, matrix, address_to_location_dict
    )

    print("NN returns:", loc, dist, pkg)

    assert pkg is not None, "NN returned None package_id"
    assert isinstance(loc, int), "Location index is not int"
    assert dist > 0, "Distance seems wrong"

    print("Nearest Neighbor: OK")

if __name__ == "__main__":
    test_nn_for_one_truck()