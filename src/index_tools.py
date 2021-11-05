import os

from aws_lambda_powertools import Logger

logger = Logger(
    service="aws-lambda-telescope-elasticsearch",
    level=os.environ.get("LOG_LEVEL", "INFO"),
)


def is_writable(index: dict) -> bool:
    logger.debug(f"index: {index}")
    try:
        try:
            return list(index.get("aliases").values())[0].get("is_write_index")
        except AttributeError:
            return False
    except IndexError:
        return False


def get_writable_indices(indices: dict) -> dict:
    logger.debug(f"Indices: {indices}")
    out = {}
    for index_name in indices:
        index = indices[index_name]
        if is_writable(index):
            out[index_name] = index
    return out


def get_number_index_fields(index_mapping: dict) -> dict:
    logger.debug(f"index_mapping: {index_mapping}")
    index_name = list(index_mapping.keys())[0]
    logger.debug(f"index: {index_name}")
    return len(index_mapping[index_name]["mappings"]["doc"].keys())


def get_number_indices_shards(indices: dict) -> dict:
    logger.debug(f"Indices: {indices}")
    out = {}
    for index_name in indices:
        index = indices[index_name]
        num_shards = get_number_of_shards(index)
        if num_shards is not None:
            out[index_name] = num_shards
    return out


def get_number_of_shards(index: dict) -> int:
    logger.debug(f"index: {index}")
    try:
        return int(index["settings"]["index"]["number_of_shards"])
    except KeyError:
        return None


def get_indices_size_in_bytes(indices: dict) -> dict:
    logger.debug(f"indices: {indices}")
    return dict(
        (k, get_index_size_in_bytes(v)) for (k, v) in indices["indices"].items()
    )


def get_index_size_in_bytes(index: dict) -> int:
    logger.debug(f"index: {index}")
    try:
        return index["total"]["store"]["size_in_bytes"]
    except KeyError:
        return None
