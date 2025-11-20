from distance_matrix import retrieve_distance
from address_to_location import address_to_location_dict


def get_nearest_neighbor(truck, package_hash_table, index_map, matrix):
    min_distance = float("inf")
    closest_location = None

    for package_ID in truck.packages:
        pkg = package_hash_table.lookup(package_ID)

        if pkg.status == "Delivered":
            continue

        # Since our distance matrix header is location names, not addresses, we convert so we can access the matrix correctly.
        adr = pkg.address
        location_name = address_to_location_dict[adr]
        pkg_location_index = index_map[location_name]

        # Obtain distance to pkg location
        distance = retrieve_distance(
            truck.current_location, pkg_location_index, matrix, index_map
        )
        # Compare current pkg to min distance, update if smaller
        if distance < min_distance:
            min_distance = distance
            closest_location = pkg_location_index

    return closest_location, min_distance


def deliver_package(truck, package_hash_table, index_map):
    for package_id in truck.packages:
        pkg = package_hash_table.lookup(package_id)

        # Since our distance matrix header is location names, not addresses, we convert so we can access the matrix correctly.
        adr = pkg.address
        location_name = address_to_location_dict[adr]
        pkg_location_index = index_map[location_name]

        # If
        if pkg_location_index == truck.current_location:
            truck.package_deliver(pkg)


def start_truck_route(truck, package_hash_table, index_map, matrix):
    for package_id in truck.packages:
        # When truck leaves hub, each package on truck gets marked En route with timestamp
        pkg = package_hash_table.lookup(package_id)
        pkg.set_status("En route", truck.departure_time)

    while True:
        # Loop through package objects in truck, see if all are delivered
        delivered = [
            pck
            for pck in truck.packages
            if package_hash_table.lookup(pck).status == "Delivered"
        ]

        if delivered:
            break

        # Calculate the nearest location, drive truck to this location and deliver package
        closest_location, min_distance = get_nearest_neighbor(
            truck, package_hash_table, index_map, matrix
        )
        truck.drive_to(closest_location, min_distance)
        deliver_package(truck, package_hash_table, index_map)

    return truck.total_mileage
