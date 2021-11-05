import os

import boto3
from aws_lambda_powertools import Logger
from elasticsearch_api import ElasticSearchAPI
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


def get_elasticsearch_credential():
    logger.debug("pulling telescope password from ssm")
    client = boto3.client("ssm")
    return client.get_parameter(
        Name="/secrets/elasticsearch/telescope_password", WithDecryption=True
    )["Parameter"]["Value"]


def derive_and_publish_elasticsearch_metrics(graphite_host: str):
    # get all indices and number of shards that fit {get_index_alias_patterns()}
    index_alias_patterns = get_index_alias_patterns()
    logger.debug(f"index aliases: {index_alias_patterns}")
    elastic_url = os.environ.get("elastic_url", "https://elasticsearch")
    logger.debug(f"elastic url: {elastic_url}")
    elasticsearch_api = ElasticSearchAPI(
        url=elastic_url, username="telescope", password=get_elasticsearch_credential()
    )
    writeable_indices = get_writable_indices(
        elasticsearch_api.get_indices(index_alias_patterns)
    )
    index_shards = get_number_indices_shards(writeable_indices)
    indices_sizes = get_indices_size_in_bytes(
        elasticsearch_api.get_indices_stats(list(writeable_indices.keys()))
    )
    indices_fields = dict(
        (
            index_name,
            get_number_index_fields(elasticsearch_api.get_index_fields(index_name)),
        )
        for index_name in writeable_indices.keys()
    )

    for index_name in index_shards:
        publish_to_graphite(
            path=f"{index_name}.number_shards",
            metrics=index_shards[index_name],
            graphite_host=graphite_host,
        )

    for index_name in indices_sizes:
        publish_to_graphite(
            path=f"{index_name}.size_in_bytes",
            metrics=indices_sizes[index_name],
            graphite_host=graphite_host,
        )

    for index_name in indices_fields:
        publish_to_graphite(
            path=f"{index_name}.number_fields",
            metrics=indices_fields[index_name],
            graphite_host=graphite_host,
        )
