import unittest

from . import test_client


class TestRequisitionsClient(unittest.TestCase):
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

    def test_create(self):
        client = test_client().requisitions

        client.create(
            **{
                "redirect": "redirect",
                "agreements": "agreements",
                "reference": "reference",
                "enduser_id": "enduser_id",
                "language": "language",
            }
        )

        client.request_strategy.post.assert_called_with(
            "https://ob.nordigen.com/api/v2/requisitions/",
            data={
                "redirect": "redirect",
                "agreements": "agreements",
                "reference": "reference",
                "enduser_id": "enduser_id",
                "user_language": "language",
            },
            params=None,
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
