from more_itertools import map_except


def get_writable(index: dict) -> bool:
    try:
        try:
            return list(index.get("aliases").values())[0].get("is_write_index")
        except AttributeError:
            return False
    except IndexError:
        return False


def get_number_writable_indices_shards(indices: dict) -> dict:
    return dict(
        (k, get_number_of_shards(v))
        for (k, v) in indices.items()
        if get_writable(v) and (get_number_of_shards(v) is not None)
    )


def get_number_of_shards(index: dict) -> int:
    try:
        return int(index["settings"]["index"]["number_of_shards"])
    except KeyError:
        return None
