import unittest

from . import test_client


class TestAspspsClient(unittest.TestCase):
    def test_by_enduser_id(self):
        client = test_client().agreements
        client.by_enduser_id(enduser_id="foobar-id")
        client.request_strategy.get.assert_called_with(
            "https://ob.nordigen.com/api/agreements/enduser/?enduser_id=foobar-id", params=None
        )

    def test_by_enduser_id_pagination(self):
        client = test_client().agreements
        client.by_enduser_id(enduser_id="foobar-id", limit=1)
        client.request_strategy.get.assert_called_with(
            "https://ob.nordigen.com/api/agreements/enduser/?enduser_id=foobar-id&limit=1", params=None
        )

        client.by_enduser_id(enduser_id="foobar-id", offset=5)
        client.request_strategy.get.assert_called_with(
            "https://ob.nordigen.com/api/agreements/enduser/?enduser_id=foobar-id&offset=5", params=None
        )

    def test_create(self):
        client = test_client().agreements
        client.create(enduser_id="foobar-id", aspsp_id="fizzbuzz-id", historical_days=45)
        client.request_strategy.post.assert_called_with(
            "https://ob.nordigen.com/api/agreements/enduser/",
            data={"max_historical_days": 45, "enduser_id": "foobar-id", "aspsp_id": "fizzbuzz-id"},
            params=None,
        )

    def test_by_id(self):
        client = test_client().agreements
        client.by_id("foobar-id")
        client.request_strategy.get.assert_called_with(
            "https://ob.nordigen.com/api/agreements/enduser/foobar-id/", params=None
        )

    def test_remove(self):
        client = test_client().agreements
        client.remove("foobar-id")
        client.request_strategy.delete.assert_called_with(
            "https://ob.nordigen.com/api/agreements/enduser/foobar-id/", params=None
        )

    def test_accept(self):
        client = test_client().agreements
        client.accept("foobar-id")
        client.request_strategy.put.assert_called_with(
            "https://ob.nordigen.com/api/agreements/enduser/foobar-id/accept/",
            data={"user_agent": "user-agent", "ip_address": "127.0.0.1"},
            params=None,
        )

    def test_text(self):
        client = test_client().agreements
        client.text("foobar-id")
        client.request_strategy.get.assert_called_with(
            "https://ob.nordigen.com/api/agreements/enduser/foobar-id/text/", params=None
        )
