import unittest

from . import _test_client, _test_client_with_token


class TestPremiumClient(unittest.TestCase):
    def test_balances(self):
        client = _test_client().premium
        client.balances("foobar-id")
        client.request_strategy.get.assert_called_with(
            "https://bankaccountdata.gocardless.com/api/v2/accounts/premium/foobar-id/balances/", params=None
        )

    def test_details(self):
        client = _test_client().premium
        client.details("foobar-id")
        client.request_strategy.get.assert_called_with(
            "https://bankaccountdata.gocardless.com/api/v2/accounts/premium/foobar-id/details/", params=None
        )

    def test_transactions(self):
        client = _test_client().premium
        client.transactions("foobar-id")
        client.request_strategy.get.assert_called_with(
            "https://bankaccountdata.gocardless.com/api/v2/accounts/premium/foobar-id/transactions/", params=None
        )


class TestPremiumClientV1(unittest.TestCase):
    def test_not_implemented(self):
        client = _test_client_with_token().premium

        with self.assertRaises(NotImplementedError):
            client.balances("foobar-id")

        with self.assertRaises(NotImplementedError):
            client.details("foobar-id")

        with self.assertRaises(NotImplementedError):
            client.transactions("foobar-id")
