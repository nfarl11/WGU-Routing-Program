from operator import ifloordiv

from distance_matrix import retrieve_distance
from address_to_location import address_to_location_dict


def get_nearest_neighbor(truck, package_hash_table, index_map, matrix):
    # In order to account for packages with deadline we will route those with priority
    has_deadline = []
    eod_deadline = []

    for package_ID in truck.packages:
        pkg = package_hash_table.lookup(str(package_ID))

        if pkg.delivery_status == "Delivered":
            continue

        if pkg.package_deadline != "EOD":
            has_deadline.append(package_ID)
        else:
            eod_deadline.append(package_ID)

    # We want to utilize "free" deliveries even if they are end of day
    deadline_closest_loc = None
    deadline_closest_dist = float("inf")

    # Find the closest package with a deadline
    for package_ID in has_deadline:
        pkg = package_hash_table.lookup(str(package_ID))
        adr = pkg.package_address
        loc_name = address_to_location_dict[adr]
        pkg_loc = index_map[loc_name]

        dist = retrieve_distance(
            truck.current_location, pkg_loc, matrix, index_map
        )

        if dist < deadline_closest_dist:
            deadline_closest_dist = dist
            deadline_closest_loc = pkg_loc

    eod_closest_loc = None
    eod_closest_dist = float("inf")

    # Find the closest package with no deadline
    for package_ID in eod_deadline:
        pkg = package_hash_table.lookup(package_ID)
        adr = pkg.address
        loc_name = address_to_location_dict[adr]
        pkg_loc = index_map[loc_name]

        dist = retrieve_distance(
            truck.current_location, pkg_loc, matrix, index_map
        )

        if dist < eod_closest_dist:
            eod_closest_dist = dist
            eod_closest_loc = pkg_loc

    # If there are no remaining deadline packages, return closest EOD package
    if not has_deadline:
        return eod_closest_loc, eod_closest_dist

    # If the EOD package is closer than deadline package, choose EOD package
    if eod_closest_dist < deadline_closest_dist:
        return eod_closest_loc, eod_closest_dist

    # Else, go to deadline package
    return deadline_closest_loc, deadline_closest_dist


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
