from unittest import TestCase

import pytest

from src.index_tools import get_indices_size_in_bytes
from src.index_tools import get_number_index_fields
from src.index_tools import get_number_indices_shards
from src.index_tools import get_writable_indices
from src.index_tools import is_writable


@pytest.fixture
def writable_indices():
    return {}


class GetIsWritable(TestCase):
    def test_get_is_writable(self):
        index = {"aliases": {"logstash-test-index": {"is_write_index": True}}}

        self.assertTrue(is_writable(index))

    def test_get_isnt_writable(self):
        index = {"aliases": {"logstash-test-index": {"is_write_index": False}}}
        self.assertFalse(is_writable(index))

    def test_no_aliases(self):
        index = {"aliases": {}}

        self.assertFalse(is_writable(index))

    def test_empty(self):
        self.assertFalse(is_writable({}))


class GetWritableIndices(TestCase):
    def test_get_writable_indices(self):
        indices = {
            "logstash-clickhouse-000010": {
                "aliases": {"logstash-clickhouse": {"is_write_index": True}},
                "settings": {"index": {"number_of_shards": "3"}},
            },
            "logstash-clickhouse-000011": {
                "aliases": {"logstash-clickhouse": {"is_write_index": False}}
            },
            "logstash-clickhouse-000012": {
                "aliases": {"logstash-clickhouse": {"is_write_index": False}}
            },
            "logstash-test-index-000020": {
                "aliases": {"logstash-test-index": {"is_write_index": True}},
                "settings": {"index": {"number_of_shards": "6"}},
            },
            "logstash-test-index-000021": {
                "aliases": {"logstash-test-index": {"is_write_index": False}}
            },
            "logstash-test-index-000022": {
                "aliases": {"logstash-test-index": {"is_write_index": False}}
            },
        }
        self.assertDictEqual(
            get_writable_indices(indices),
            {
                "logstash-clickhouse-000010": {
                    "aliases": {"logstash-clickhouse": {"is_write_index": True}},
                    "settings": {"index": {"number_of_shards": "3"}},
                },
                "logstash-test-index-000020": {
                    "aliases": {"logstash-test-index": {"is_write_index": True}},
                    "settings": {"index": {"number_of_shards": "6"}},
                },
            },
        )

    def test_get_no_writable_indices(self):
        indices = {}
        self.assertDictEqual(get_number_indices_shards(indices), {})


class GetIndicesShards(TestCase):
    def test_get_number_indices_shards(self):
        indices = {
            "logstash-clickhouse-000010": {
                "settings": {"index": {"number_of_shards": "3"}},
            },
            "logstash-test-index-000020": {
                "settings": {"index": {"number_of_shards": "6"}},
            },
        }
        self.assertDictEqual(
            get_number_indices_shards(indices),
            {
                "logstash-test-index-000020": 6,
                "logstash-clickhouse-000010": 3,
            },
        )

    def test_get_no_indices_shards(self):
        indices = {}
        self.assertDictEqual(get_number_indices_shards(indices), {})

    def test_get_no_index_settings(self):
        indices = {
            "logstash-clickhouse-000010": {
                "aliases": {"logstash-clickhouse": {"is_write_index": True}}
            }
        }
        self.assertDictEqual(get_number_indices_shards(indices), {})


class GetIndicesSize(TestCase):
    def test_get_indices_size(self):
        indices = {
            "indices": {
                "logstash-cloudwatch-000678": {
                    "total": {"store": {"size_in_bytes": 123456789}}
                }
            }
        }
        self.assertDictEqual(
            get_indices_size_in_bytes(indices),
            {"logstash-cloudwatch-000678": 123456789},
        )


class GetIndexFields(TestCase):
    def test_get_index_fields_es7(self):
        index = {
            "logstash-cloudwatch-000678": {
                "mappings": {"@timestamp": {}, "log": {}, "message": {}}
            }
        }
        self.assertEqual(
            get_number_index_fields(index),
            3,
        )

    def test_get_index_fields_es6(self):
        index = {
            "logstash-cloudwatch-000678": {
                "mappings": {"doc": {"@timestamp": {}, "log": {}, "message": {}}}
            }
        }
        self.assertEqual(
            get_number_index_fields(index),
            3,
        )
