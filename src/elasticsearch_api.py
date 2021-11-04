import os

import requests
from aws_lambda_powertools import Logger

logger = Logger(
    service="aws-lambda-telescope-elasticsearch",
    level=os.environ.get("LOG_LEVEL", "INFO"),
)


def get_indices(url: str, pattern: str) -> dict:
    logger.debug(pattern)
    return requests.get(f"{url}/{pattern}").json()


def get_indices_stats(url: str, index_names: list) -> dict:
    logger.debug(index_names)
    return requests.get(f"{url}/{','.join(index_names)}/_stats").json()


def get_index_fields(url: str, index_name: str) -> dict:
    logger.debug(index_name)
    return requests.get(f"{url}/{index_name}/_mapping/field/*").json()
