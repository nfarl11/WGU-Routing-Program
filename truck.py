from datetime import timedelta
from logging import exception

truck_speed = 18  # mph


class Truck:
    def __init__(self, truck_number, departure_time, capacity=16):
        self.truck_number = truck_number
        self.departure_time = departure_time
        self.packages = []
        self.current_location = 0
        self.capacity = capacity
        self.total_mileage = 0.0
        self.current_time = departure_time

    def add_package(self, package_id: str):
        # If the truck is not at capacity, a new package will be appended
        if len(self.packages) < self.capacity:
            self.packages.append(package_id)
        else:
            raise exception("Truck is at capacity")

    def drive_to(self, next_location, distance):
        # Changes the location of the truck and updates mileage
        self.total_mileage += distance
        self.current_location = next_location

        # Calculate the time spent driving and use timedelta to add driving time to current time
        hours_traveled = distance / truck_speed
        time_delta = timedelta(hours=hours_traveled)
        self.current_time += time_delta

    def package_deliver(self, pack_obj):
        pack_obj.set_status("Delivered", self.current_time)

    def __str__(self):
        return (
            f"{self.truck_number}, Packages: {self.packages}, "
            f"Time: {self.current_time}, "
            f"Total Mileage: {self.total_mileage}, "
            f"Current Stop: {self.current_location}"
        )
