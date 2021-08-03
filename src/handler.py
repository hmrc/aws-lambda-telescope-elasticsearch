from src.send_graphyte_message import publish_to_graphite
from src.index_tools import (
    get_indices_size_in_bytes,
    get_number_writable_indices_shards,
)
from src.elasticsearch_api import get_indices, get_indices_stats
from aws_lambda_powertools import Logger
import os

logger = Logger(
    service="aws-lambda-telescope-elasticsearch",
    level=os.environ.get("LOG_LEVEL", "INFO"),
)


def get_graphite_host():
    return os.environ.get("graphite_host", "graphite")


def get_index_alias_patterns():
    return os.environ.get("index_alias_patterns", "")


def lambda_handler(event, context):
    try:
        logger.info(f"Lambda Request ID: {context.aws_request_id}")
    except AttributeError:
        logger.debug(f"No context object available")

    graphite_host = get_graphite_host()
    derive_and_publish_elasticsearch_metrics(graphite_host)


def derive_and_publish_elasticsearch_metrics(graphite_host: str):
    # get all indices and number of shards that fit {get_index_alias_patterns()}
    index_alias_patterns = get_index_alias_patterns()
    elastic_url = os.environ.get("elastic_url", "https://elasticsearch")
    index_shards = get_number_writable_indices_shards(
        get_indices(elastic_url, index_alias_patterns)
    )
    indices_sizes = get_indices_size_in_bytes(
        get_indices_stats(elastic_url, list(index_shards.keys()))
    )

    for index_name in index_shards:
        publish_to_graphite(
            f"{index_name}.number_shards", index_shards[index_name], graphite_host
        )

    for index_name in indices_sizes:
        publish_to_graphite(
            f"{index_name}.size_in_bytes", indices_sizes[index_name], graphite_host
        )
