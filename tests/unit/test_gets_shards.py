from unittest import TestCase


class GetIsWritable(TestCase):
    def get_is_writable(self):
        index = {
            "aliases": {"logstash-test-index": {"is_write_index": True}},
            "settings": {"index": {"number_of_shards": "3"}},
        }

        self.assertTrue(get_writable(index))


# class GetShards(TestCase):
