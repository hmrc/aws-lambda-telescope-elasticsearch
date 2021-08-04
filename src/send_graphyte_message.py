import graphyte
from app_info import METRICS_PREFIX


def publish_to_graphite(path, metrics, graphite_host):
    graphyte.init(graphite_host, prefix=METRICS_PREFIX)
    graphyte.send(path, metrics)
