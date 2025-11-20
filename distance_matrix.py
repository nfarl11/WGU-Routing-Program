def build_address_dict(locations):
    mapping = {}
    for index, name in enumerate(locations):
        mapping[name.strip()] = index
    return mapping


def retrieve_distance(location1, location2, matrix, mapping):
    i = mapping[location1]
    j = mapping[location2]
    return matrix[i][j]
