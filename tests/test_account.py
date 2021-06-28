import unittest

from . import test_client


class TestAccountClient(unittest.TestCase):
    def test_info(self):
        client = test_client().account
        client.info("foobar-id")
        client.request_strategy.get.assert_called_with("https://ob.nordigen.com/api/accounts/foobar-id/", params=None)

    def test_balances(self):
        client = test_client().account
        client.balances("foobar-id")
        client.request_strategy.get.assert_called_with(
            "https://ob.nordigen.com/api/accounts/foobar-id/balances/", params=None
        )

    def test_details(self):
        client = test_client().account
        client.details("foobar-id")
        client.request_strategy.get.assert_called_with(
            "https://ob.nordigen.com/api/accounts/foobar-id/details/", params=None
        )

    def test_transactions(self):
        client = test_client().account
        client.transactions("foobar-id")
        client.request_strategy.get.assert_called_with(
            "https://ob.nordigen.com/api/accounts/foobar-id/transactions/", params=None
        )
