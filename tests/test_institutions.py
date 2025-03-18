import unittest

from . import _test_client


class TestInstitutionsClient(unittest.TestCase):
    def test_by_country(self):
        client = _test_client().institutions
        client.by_country("SE")

        client.request_strategy.get.assert_called_with(
            "https://bankaccountdata.gocardless.com/api/v2/institutions/?country=SE", params=None
        )

    def test_by_id_v1(self):
        client = _test_client().institutions
        client.by_id("foo-bar-id")

        client.request_strategy.get.assert_called_with(
            "https://bankaccountdata.gocardless.com/api/v2/institutions/foo-bar-id/", params=None
        )
