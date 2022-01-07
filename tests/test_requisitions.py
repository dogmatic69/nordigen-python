import unittest
from unittest.mock import patch

from . import test_client, test_client_with_token


class TestRequisitionsClientV1(unittest.TestCase):
    def test_create_v1(self):
        client = test_client_with_token().requisitions

        with self.assertWarns(DeprecationWarning) as warn:
            client.create(
                **{
                    "redirect": "redirect",
                    "agreements": "agreements",
                    "reference": "reference",
                    "enduser_id": "enduser_id",
                    "language": "language",
                }
            )

        expected = "RequisitionsClient().create() has breaking changes in V2"
        assert str(warn.warning) == expected

        client.request_strategy.post.assert_called_with(
            "https://ob.nordigen.com/api/requisitions/",
            data={
                "redirect": "redirect",
                "agreements": "agreements",
                "reference": "reference",
                "enduser_id": "enduser_id",
                "user_language": "language",
            },
            params=None,
        )

    def test_create_v2_not_implemented(self):
        client = test_client_with_token().requisitions

        with self.assertRaises(NotImplementedError):
            client.create_v2(redirect=None, institution_id=None, reference=None)

    def test_create_without_aspsp_id_value_error(self):
        client = test_client_with_token().requisitions

        with self.assertWarns(DeprecationWarning):
            with self.assertRaises(ValueError):
                client.create(redirect=None, reference=None)


class TestRequisitionsClient(unittest.TestCase):
    @patch("nordigen.client.RequisitionsClient.create_v2")
    def test_create_calls_create_v2(self, mocked_v2):
        client = test_client().requisitions

        with self.assertWarns(DeprecationWarning) as warn:
            client.create(
                **{
                    "redirect": "redirect",
                    "institution_id": "institution_id",
                    "reference": "reference",
                }
            )

        expected = "RequisitionsClient().create() has breaking changes in V2"
        assert str(warn.warning) == expected

        mocked_v2.assert_called_with(
            redirect="redirect", reference="reference", institution_id="institution_id", language=None
        )

    def test_create_v2_defaults(self):
        client = test_client().requisitions

        client.create_v2(
            **{
                "redirect": "redirect",
                "institution_id": "institution_id",
                "reference": "reference",
            }
        )
        client.request_strategy.post.assert_called_with(
            "https://ob.nordigen.com/api/v2/requisitions/",
            data={
                "redirect": "redirect",
                "institution_id": "institution_id",
                "reference": "reference",
                "account_selection": False,
            },
            params=None,
        )

    def test_create_v2_options(self):
        client = test_client().requisitions

        client.create_v2(
            **{
                "redirect": "redirect",
                "institution_id": "institution_id",
                "reference": "reference",
                "agreement": "agreement",
                "account_selection": True,
                "language": "language",
                "ssn": "ssn",
            }
        )
        client.request_strategy.post.assert_called_with(
            "https://ob.nordigen.com/api/v2/requisitions/",
            data={
                "redirect": "redirect",
                "institution_id": "institution_id",
                "reference": "reference",
                "agreement": "agreement",
                "account_selection": True,
                "user_language": "language",
                "ssn": "ssn",
            },
            params=None,
        )

    def test_list(self):
        client = test_client().requisitions

        client.list()
        client.request_strategy.get.assert_called_with("https://ob.nordigen.com/api/v2/requisitions/", params=None)

        client.list(limit=1)
        client.request_strategy.get.assert_called_with(
            "https://ob.nordigen.com/api/v2/requisitions/?limit=1", params=None
        )

        client.list(offset=5)
        client.request_strategy.get.assert_called_with(
            "https://ob.nordigen.com/api/v2/requisitions/?offset=5", params=None
        )

    def test_by_id(self):
        client = test_client().requisitions

        client.by_id("foobar-id")
        client.request_strategy.get.assert_called_with(
            "https://ob.nordigen.com/api/v2/requisitions/foobar-id/", params=None
        )

    def test_remove(self):
        client = test_client().requisitions

        client.remove("foobar-id")
        client.request_strategy.delete.assert_called_with(
            "https://ob.nordigen.com/api/v2/requisitions/foobar-id/", params=None
        )

    def test_initiate(self):
        client = test_client().requisitions

        client.initiate("foobar-id", "aspsp_id")
        client.request_strategy.post.assert_called_with(
            "https://ob.nordigen.com/api/v2/requisitions/foobar-id/links/",
            data={
                "aspsp_id": "aspsp_id",
            },
            params=None,
        )
