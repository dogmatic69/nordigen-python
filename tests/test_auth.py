import unittest

from . import test_client


class TestAuthClient(unittest.TestCase):
    def test_token(self):
        client = test_client().aspsps.get_authentication_method()._client
        client.token(secret_id="secret_id", secret_key="secret_key")
        client.request_strategy.post.assert_called_with(
            "https://ob.nordigen.com/api/v2/token/new/",
            data={
                "secret_id": "secret_id",
                "secret_key": "secret_key",
            },
            params=None,
        )

    def test_refresh(self):
        client = test_client().aspsps.get_authentication_method()._client
        client.refresh(refresh_token="refresh_token")
        client.request_strategy.post.assert_called_with(
            "https://ob.nordigen.com/api/v2/token/refresh/",
            data={
                "refresh_token": "refresh_token",
            },
            params=None,
        )
