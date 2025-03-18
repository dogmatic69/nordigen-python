import unittest

from . import _test_client, _test_client_with_token


class TestAgreementsClientV1(unittest.TestCase):
    def test_by_enduser_id_v1(self):
        client = _test_client_with_token().agreements

        with self.assertWarns(DeprecationWarning) as warn:
            client.by_enduser_id(enduser_id="foobar-id")
            client.request_strategy.get.assert_called_with(
                "https://bankaccountdata.gocardless.com/api/agreements/enduser/?enduser_id=foobar-id", params=None
            )

        expected = "list by enduser_id is not supported in v2, fetch all with AgreementsClient().list()"
        assert str(warn.warning) == expected

    def test_by_enduser_id_pagination_v1(self):
        client = _test_client_with_token().agreements

        with self.assertWarns(DeprecationWarning) as warn:
            client.by_enduser_id(enduser_id="foobar-id", limit=1)
            client.request_strategy.get.assert_called_with(
                "https://bankaccountdata.gocardless.com/api/agreements/enduser/?enduser_id=foobar-id&limit=1",
                params=None,
            )

        expected = "list by enduser_id is not supported in v2, fetch all with AgreementsClient().list()"
        assert str(warn.warning) == expected

        with self.assertWarns(DeprecationWarning):
            client.by_enduser_id(enduser_id="foobar-id", offset=8)
            client.request_strategy.get.assert_called_with(
                "https://bankaccountdata.gocardless.com/api/agreements/enduser/?enduser_id=foobar-id&offset=8",
                params=None,
            )

    def test_create_v1(self):
        client = _test_client_with_token().agreements
        client.create(enduser_id="foobar-id", aspsp_id="fizzbuzz-id", historical_days=45)

        client.request_strategy.post.assert_called_with(
            "https://bankaccountdata.gocardless.com/api/agreements/enduser/",
            data={"max_historical_days": 45, "enduser_id": "foobar-id", "aspsp_id": "fizzbuzz-id"},
            params=None,
        )

    def test_create_without_enduser_id_v1(self):
        client = _test_client_with_token().agreements

        with self.assertRaises(ValueError):
            client.create(aspsp_id="foobar-id")

    def test_text_v1(self):
        client = _test_client_with_token().agreements

        with self.assertWarns(DeprecationWarning) as warn:
            client.text("foobar-id")

        expected = "AgreementsClient().text() has been removed in V2"
        assert str(warn.warning) == expected

        client.request_strategy.get.assert_called_with(
            "https://bankaccountdata.gocardless.com/api/agreements/enduser/foobar-id/text/", params=None
        )

    def test_list_not_implemented_v1(self):
        client = _test_client_with_token().agreements

        with self.assertRaises(NotImplementedError):
            client.list()

    def test_create_requires_aspsp_id_v1(self):
        client = _test_client_with_token().agreements

        with self.assertRaises(ValueError):
            client.create(enduser_id="foobar-id")


class TestAgreementsClient(unittest.TestCase):
    def test_by_enduser_id(self):
        client = _test_client().agreements

        with self.assertWarns(DeprecationWarning) as warn:
            client.by_enduser_id(enduser_id="foobar-id")
            client.request_strategy.get.assert_called_with(
                "https://bankaccountdata.gocardless.com/api/v2/agreements/enduser/", params=None
            )
        expected = "list by enduser_id is not supported in v2, fetch all with AgreementsClient().list()"
        assert str(warn.warning) == expected

    def test_by_enduser_id_pagination(self):
        client = _test_client().agreements

        with self.assertWarns(DeprecationWarning) as warn:
            client.by_enduser_id(enduser_id="foobar-id", limit=1)
            client.request_strategy.get.assert_called_with(
                "https://bankaccountdata.gocardless.com/api/v2/agreements/enduser/?limit=1", params=None
            )

        expected = "list by enduser_id is not supported in v2, fetch all with AgreementsClient().list()"
        assert str(warn.warning) == expected

        with self.assertWarns(DeprecationWarning):
            client.by_enduser_id(enduser_id="foobar-id", offset=5)
            client.request_strategy.get.assert_called_with(
                "https://bankaccountdata.gocardless.com/api/v2/agreements/enduser/?offset=5", params=None
            )

    def test_text_not_implemented(self):
        client = _test_client().agreements

        with self.assertWarns(DeprecationWarning):
            with self.assertRaises(NotImplementedError):
                client.text("foobar-id")

    def test_create(self):
        client = _test_client().agreements
        with self.assertWarns(DeprecationWarning) as warn:
            client.create(aspsp_id="fizzbuzz-id", historical_days=45)

        client.request_strategy.post.assert_called_with(
            "https://bankaccountdata.gocardless.com/api/v2/agreements/enduser/",
            data={
                "max_historical_days": 45,
                "access_valid_for_days": 30,
                "access_scope": ["transactions", "balances", "details"],
                "institution_id": "fizzbuzz-id",
            },
            params=None,
        )

        expected = "aspsp_id is deprecated in v2"
        assert str(warn.warning) == expected

    def test_create_with_enduser_raises_exception_id(self):
        client = _test_client().agreements

        with self.assertRaises(ValueError):
            client.create(enduser_id="foobar-id")

    def test_create_with_no_args_raises_exception(self):
        client = _test_client().agreements

        with self.assertRaises(ValueError):
            client.create()

    def test_by_id(self):
        client = _test_client().agreements
        client.by_id("foobar-id")
        client.request_strategy.get.assert_called_with(
            "https://bankaccountdata.gocardless.com/api/v2/agreements/enduser/foobar-id/", params=None
        )

    def test_remove(self):
        client = _test_client().agreements
        client.remove("foobar-id")
        client.request_strategy.delete.assert_called_with(
            "https://bankaccountdata.gocardless.com/api/v2/agreements/enduser/foobar-id/", params=None
        )

    def test_accept(self):
        client = _test_client().agreements
        client.accept("foobar-id")
        client.request_strategy.put.assert_called_with(
            "https://bankaccountdata.gocardless.com/api/v2/agreements/enduser/foobar-id/accept/",
            data={"user_agent": "user-agent", "ip_address": "127.0.0.1"},
            params=None,
        )
