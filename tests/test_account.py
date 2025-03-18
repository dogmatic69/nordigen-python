import unittest
from unittest.mock import Mock

from apiclient.request_strategies import BaseRequestStrategy

from . import _test_client


class TestAccountClient(unittest.TestCase):
    def test_info(self):
        client = _test_client().account
        client.info("foobar-id")
        client.request_strategy.get.assert_called_with(
            "https://bankaccountdata.gocardless.com/api/v2/accounts/foobar-id/", params=None
        )

    def test_balances(self):
        client = _test_client().account
        client.balances("foobar-id")
        client.request_strategy.get.assert_called_with(
            "https://bankaccountdata.gocardless.com/api/v2/accounts/foobar-id/balances/", params=None
        )

    def test_details(self):
        client = _test_client().account
        client.details("foobar-id")
        client.request_strategy.get.assert_called_with(
            "https://bankaccountdata.gocardless.com/api/v2/accounts/foobar-id/details/", params=None
        )

    def test_transactions(self):
        client = _test_client().account
        client.transactions("foobar-id")
        client.request_strategy.get.assert_called_with(
            "https://bankaccountdata.gocardless.com/api/v2/accounts/foobar-id/transactions/", params=None
        )


class TestAccountClientErrors(unittest.TestCase):
    def test_info(self):
        client = _test_client(request_strategy=Mock(spec=BaseRequestStrategy)).account
        client.info("foobar-id")

        # mock urllib3.connectionpool._make_request and raise an exception
        client.request_strategy.get.side_effect = Exception("test")
