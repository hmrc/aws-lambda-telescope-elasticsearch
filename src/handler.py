import os

from aws_lambda_powertools import Logger
from elasticsearch_api import get_index_fields
from elasticsearch_api import get_indices
from elasticsearch_api import get_indices_stats
from index_tools import get_indices_size_in_bytes
from index_tools import get_number_index_fields
from index_tools import get_number_indices_shards
from index_tools import get_writable_indices
from send_graphyte_message import publish_to_graphite

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
    writeable_indices = get_writable_indices(
        get_indices(elastic_url, index_alias_patterns)
    )
    index_shards = get_number_indices_shards(writeable_indices)
    indices_sizes = get_indices_size_in_bytes(
        get_indices_stats(elastic_url, list(writeable_indices.keys()))
    )
    indices_fields = [
        {index_name: get_number_index_fields(get_index_fields(elastic_url, index_name))}
        for index_name in writeable_indices.keys()
    ]

    for index_name in index_shards:
        publish_to_graphite(
            f"{index_name}.number_shards", index_shards[index_name], graphite_host
        )

    for index_name in indices_sizes:
        publish_to_graphite(
            f"{index_name}.size_in_bytes", indices_sizes[index_name], graphite_host
        )

    for index_name in indices_fields:
        publish_to_graphite(
            f"{index_name}.number_fields", indices_fields[index_name], graphite_host
        )
