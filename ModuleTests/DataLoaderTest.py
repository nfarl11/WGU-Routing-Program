from data_loader import load_packages

def test_load_packages():
    table = load_packages("../data/fresh_package_file.csv")

    # Does table contain all 40 packages?
    all_packages = [table.lookup(str(i)) for i in range(1, 41)]
    assert None not in all_packages, "Some packages did not load"

    # Spot check a known package
    p1 = table.lookup("1")
    assert p1.package_address == "195 W Oakland Ave"

    print("Package loader: OK")

if __name__ == "__main__":
    test_load_packages()
    print("Package loader: OK")