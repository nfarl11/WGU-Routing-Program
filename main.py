from data_loader import load_packages, load_distances
from distance_matrix import build_address_dict

locations, matrix = load_distances()
address_to_index = build_address_dict(locations)

print (address_to_index)
