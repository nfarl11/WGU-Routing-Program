
def build_address_dict(locations):
    mapping = {}
    for index, name in enumerate(locations):
        mapping[name.strip()] = index
    return mapping

