import unittest

from . import _test_client_with_token


class TestAspspsClient(unittest.TestCase):
    def test_by_country_v1(self):
        client = _test_client_with_token().aspsps

        with self.assertWarns(DeprecationWarning) as warn:
            client.by_country("SE")

        expected = "AspspsClient() has been replaced by InstitutionsClient() in V2"
        assert str(warn.warning) == expected

        client.request_strategy.get.assert_called_with(
            "https://bankaccountdata.gocardless.com/api/aspsps/?country=SE", params=None
        )

    def test_by_id_v1(self):
        client = _test_client_with_token().aspsps

        with self.assertWarns(DeprecationWarning) as warn:
            client.by_id("foo-bar-id")

        expected = "AspspsClient() has been replaced by InstitutionsClient() in V2"
        assert str(warn.warning) == expected

        client.request_strategy.get.assert_called_with(
            "https://bankaccountdata.gocardless.com/api/aspsps/foo-bar-id/", params=None
        )
