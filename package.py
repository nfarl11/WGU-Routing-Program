from datetime import datetime


class Package:
    def __init__(
        self,
        package_id,
        package_address,
        package_city,
        package_state,
        package_zip,
        package_deadline,
        package_weight,
        package_notes,
        delivery_status="At hub",
    ):
        self.package_id = package_id
        self.package_address = package_address
        self.package_zip = package_zip
        self.package_deadline = package_deadline
        self.delivery_status = delivery_status
        self.time_of_delivery = None
        self.package_city = package_city
        self.package_weight = package_weight
        self.package_state = package_state
        self.time_of_departure = None
        self.truck_number = None
        self.time_of_arrival = None
        self.package_notes = package_notes.strip()

        # Created new logic to collect the package notes field and adjust time of arrival based on this
        if "Delayed" in self.package_notes:
            self.time_of_arrival = datetime.strptime("09:05 AM", "%I:%M %p")
        else:
            self.time_of_arrival = datetime.strptime("08:00 AM", "%I:%M %p")

    def set_status(self, delivery_status, timestamp=None):
        self.delivery_status = delivery_status
        if timestamp:
            self.time_of_delivery = timestamp

    def __str__(self):  # Return package details
        return (
            f"Package ID: {self.package_id} - {self.package_address}, "
            f"{self.package_city}, {self.package_zip}, "
            f"Deadline: {self.package_deadline}, "
            f"Status: {self.delivery_status}, "
            f"Weight: {self.package_weight}"
        )
