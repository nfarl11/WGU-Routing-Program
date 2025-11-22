def build_address_dict(locations):
    mapping = {}
    for index, name in enumerate(locations):
        mapping[name.strip()] = index
    return mapping


def retrieve_distance(i, j, matrix, mapping=None):
    return matrix[i][j]
