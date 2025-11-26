from address_to_location import address_to_location_dict
import os

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PACKAGE_PATH = os.path.join(BASE, "data", "fresh_package_file.csv")


def test_address_mapping():
    # Test a known mapping
    assert (
        address_to_location_dict["195 W Oakland Ave"] == "South Salt Lake Public Works"
    )

    # Test that all package addresses exist in the map
    missing = []
    import csv

    with open(PACKAGE_PATH) as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            addr = row[1]
            if addr not in address_to_location_dict:
                missing.append(addr)

    assert not missing, f"Missing mappings for addresses: {missing}"

    print("Address mapping: OK")


if __name__ == "__main__":
    test_address_mapping()
    print("Address mapping: OK")
