from unittest import TestCase
from src.index_tools import get_writable


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
