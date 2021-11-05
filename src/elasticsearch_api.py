import os

import requests
from aws_lambda_powertools import Logger
from requests.auth import HTTPBasicAuth

logger = Logger(
    service="aws-lambda-telescope-elasticsearch",
    level=os.environ.get("LOG_LEVEL", "INFO"),
)


class ElasticSearchAPI(object):
    def __init__(self, url, username, password):
        self.url = url
        self.auth = HTTPBasicAuth(username, password)

    def get_indices(self, pattern: str) -> dict:
        logger.debug(pattern)
        return requests.get(f"{self.url}/{pattern}", auth=self.auth).json()

    def get_indices_stats(self, index_names: list) -> dict:
        logger.debug(index_names)
        return requests.get(
            f"{self.url}/{','.join(index_names)}/_stats", auth=self.auth
        ).json()

    def get_index_fields(self, index_name: str) -> dict:
        logger.debug(index_name)
        return requests.get(
            f"{self.url}/{index_name}/_mapping/field/*", auth=self.auth
        ).json()
