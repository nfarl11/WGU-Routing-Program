from distance_matrix import retrieve_distance


def get_nearest_neighbor(
    truck, package_hash_table, index_map, matrix, address_to_location_dict
):
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
    deadline_closest_package_id = None

    # Find the closest package with a deadline
    for package_ID in has_deadline:
        pkg = package_hash_table.lookup(str(package_ID))
        adr = pkg.package_address
        loc_name = address_to_location_dict[adr]
        pkg_loc = index_map[loc_name]

        dist = retrieve_distance(truck.current_location, pkg_loc, matrix)

        if dist < deadline_closest_dist:
            deadline_closest_dist = dist
            deadline_closest_loc = pkg_loc
            deadline_closest_package_id = package_ID

    eod_closest_loc = None
    eod_closest_dist = float("inf")
    eod_closest_package_id = None

    # Find the closest package with no deadline
    for package_ID in eod_deadline:
        pkg = package_hash_table.lookup(str(package_ID))
        adr = pkg.package_address
        loc_name = address_to_location_dict[adr]
        pkg_loc = index_map[loc_name]

        dist = retrieve_distance(truck.current_location, pkg_loc, matrix, index_map)

        if dist < eod_closest_dist:
            eod_closest_dist = dist
            eod_closest_loc = pkg_loc
            eod_closest_package_id = package_ID

    # If there are no remaining deadline packages, return closest EOD package
    if not has_deadline:
        return eod_closest_loc, eod_closest_dist, eod_closest_package_id

    # If the EOD package less than half the deadline distance, choose EOD package
    if eod_closest_dist < 0.5 * deadline_closest_dist:
        return eod_closest_loc, eod_closest_dist, eod_closest_package_id

    # Else, go to deadline package
    return deadline_closest_loc, deadline_closest_dist, deadline_closest_package_id


def start_truck_route(
    truck, package_hash_table, index_map, matrix, address_to_location_dict
):

    for package_id in truck.packages:
        pkg = package_hash_table.lookup(str(package_id))
        pkg.time_of_departure = truck.current_time
        pkg.truck_number = truck.truck_number

    while True:
        # Loop through package objects in truck, see if all are delivered
        undelivered = [
            pck
            for pck in truck.packages
            if package_hash_table.lookup(str(pck)).delivery_status != "Delivered"
        ]

        # Stop loop when all packages are delivered
        if not undelivered:
            break

        # Calculate the nearest location, drive truck to this location and deliver package
        closest_location, min_distance, closest_package_id = get_nearest_neighbor(
            truck, package_hash_table, index_map, matrix, address_to_location_dict
        )
        truck.drive_to(closest_location, min_distance)
        pkg = package_hash_table.lookup(str(closest_package_id))
        truck.package_deliver(pkg)

    if truck.current_location != 0:
        truck.return_to_hub(matrix, index_map)

    return truck.total_mileage, truck.current_time
