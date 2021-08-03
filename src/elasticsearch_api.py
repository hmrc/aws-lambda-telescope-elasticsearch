import requests


def get_indices(url: str, pattern: str) -> dict:
    print(pattern)
    return requests.get(f"{url}/{pattern}")


def get_indices_stats(url: str, index_names: list) -> dict:
    print(index_names)
    return requests.get(f"{url}/{','.join(index_names)}/_stats")
