import os
from data_loader import load_distances

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PACKAGE_PATH = os.path.join(BASE, "data", "fresh_distance_table.csv")


def test_load_distances():
    locations, matrix = load_distances(PACKAGE_PATH)

    assert len(locations) == 27
    assert len(matrix) == 27
    assert len(matrix[0]) == 27

    # Check symmetry (matrix must be mirrored)
    assert matrix[0][1] == matrix[1][0]
    assert matrix[5][7] == matrix[7][5]

    print("Distance matrix: OK")


if __name__ == "__main__":
    test_load_distances()
