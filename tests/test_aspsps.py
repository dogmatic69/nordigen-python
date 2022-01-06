import unittest

from . import test_client


class TestAspspsClient(unittest.TestCase):
    def test_by_country(self):
        client = test_client().aspsps
        client.by_country("SE")
        client.request_strategy.get.assert_called_with("https://ob.nordigen.com/api/v2/aspsps/?country=SE", params=None)

    def test_by_id(self):
        client = test_client().aspsps
        client.by_id("foo-bar-id")
        client.request_strategy.get.assert_called_with("https://ob.nordigen.com/api/v2/aspsps/foo-bar-id/", params=None)
