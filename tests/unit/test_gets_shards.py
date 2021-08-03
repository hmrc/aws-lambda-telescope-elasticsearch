import unittest
import pytest
from unittest import TestCase
from src.index_tools import get_writable, get_writable_indices


@pytest.fixture
def writable_indices():
    return {}


class GetIsWritable(TestCase):
    def test_get_is_writable(self):
        index = {"aliases": {"logstash-test-index": {"is_write_index": True}}}

        self.assertTrue(get_writable(index))

    def test_get_isnt_writable(self):
        index = {"aliases": {"logstash-test-index": {"is_write_index": False}}}
        self.assertFalse(get_writable(index))

    def test_no_aliases(self):
        index = {"aliases": {}}

        self.assertFalse(get_writable(index))

    def test_empty(self):
        self.assertFalse(get_writable({}))


class GetWritableIndices(TestCase):
    def test_get_writeable_indices(self):
        indices = {
            "logstash-clickhouse-000010": {
                "aliases": {"logstash-clickhouse": {"is_write_index": True}}
            },
            "logstash-clickhouse-000011": {
                "aliases": {"logstash-clickhouse": {"is_write_index": False}}
            },
            "logstash-clickhouse-000012": {
                "aliases": {"logstash-clickhouse": {"is_write_index": False}}
            },
            "logstash-test-index-000020": {
                "aliases": {"logstash-test-index": {"is_write_index": True}}
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
                "logstash-test-index-000020": {
                    "aliases": {"logstash-test-index": {"is_write_index": True}}
                },
                "logstash-clickhouse-000010": {
                    "aliases": {"logstash-clickhouse": {"is_write_index": True}}
                },
            },
        )

    def test_get_no_writeable_indices(self):
        indices = {}
        self.assertDictEqual(get_writable_indices(indices), {})
