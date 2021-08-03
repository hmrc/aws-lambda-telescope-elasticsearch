def get_writable(index: dict) -> bool:
    try:
        try:
            return list(index.get("aliases").values())[0].get("is_write_index")
        except AttributeError:
            return False
    except IndexError:
        return False


def get_number_writable_indices_shards(indices: dict) -> dict:
    out = {}
    for index_name in indices:
        index = indices[index_name]
        if get_writable(index):
            num_shards = get_number_of_shards(index)
            if num_shards is not None:
                out[index_name] = num_shards
    return out


def get_number_of_shards(index: dict) -> int:
    try:
        return int(index["settings"]["index"]["number_of_shards"])
    except KeyError:
        return None


def get_indices_size_in_bytes(indices: dict) -> dict:
    return dict(
        (k, get_index_size_in_bytes(v)) for (k, v) in indices["indices"].items()
    )


def get_index_size_in_bytes(index: dict) -> int:
    try:
        return index["total"]["store"]["size_in_bytes"]
    except KeyError:
        return None
