import unittest
from unittest.mock import Mock, patch

from nordigen.oauth import OAuthAuthentication


class TestOAuthAuthentication(unittest.TestCase):
    def test_perform_initial_auth(self):
        auth = OAuthAuthentication(
            expiry_margin=999,
            body={},
            client="client",
        )

        assert auth._client == "client"

    def test_valid_token_does_not_refresh(self):
        mocked_client = Mock()
        auth = OAuthAuthentication(
            expiry_margin=999,
            body={},
            client=mocked_client,
        )

        auth._token_expiration = 99999999999

        assert auth.refresh_token() is True

        mocked_client.token.assert_not_called()
        mocked_client.refresh.assert_not_called()

    @patch("nordigen.oauth.time")
    def test_expired_token_refreshes(self, mocked_time):
        mocked_time.return_value = 1234.567
        mocked_client = Mock()
        mocked_client.refresh.return_value = {
            "access": "access-token-yeahaw",
            "access_expires": 50,  # expires in 50 seconds
        }

        auth = OAuthAuthentication(
            expiry_margin=999,
            body={"foo": "bar"},
            client=mocked_client,
        )

        auth._refresh_expiration = 1250
        auth._refresh_token = "super-refresh-token"

        assert auth._access_token is None
        assert auth._token_expiration is None

        assert auth.refresh_token() is True

        mocked_client.refresh.assert_called_once_with(refresh_token="super-refresh-token")

        assert auth._access_token == "access-token-yeahaw"
        assert auth._token_expiration == 1234 + 50 - 999

    @patch("nordigen.oauth.time")
    def test_expired_refresh_token(self, mocked_time):
        mocked_time.return_value = 1234.567
        mocked_client = Mock()
        mocked_client.token.return_value = {
            "access": "access-token-yeahaw",
            "access_expires": 50,  # expires in 50 seconds
            "refresh": "refresh-token-yeahaw",
            "refresh_expires": 60,  # expires in 60 seconds
        }

        auth = OAuthAuthentication(
            expiry_margin=1,
            body={"foo": "bar"},
            client=mocked_client,
        )

        auth._refresh_expiration = 1200  # expired 34 seconds ago
        auth._refresh_token = "super-old-refresh-token"
        auth._token_expiration = 1200  # expired 34 seconds ago
        auth._access_token = "super-old-access-token"

        assert auth.refresh_token() is None

        mocked_client.token.assert_called_once_with(foo="bar")

        assert auth._access_token == "access-token-yeahaw"
        assert auth._token_expiration == 1234 + 50 - 1
        assert auth._refresh_token == "refresh-token-yeahaw"
        assert auth._refresh_expiration == 1234 + 60 - 1

    @patch("nordigen.oauth.time")
    def test_get_headers(self, mocked_time):
        mocked_time.return_value = 1234.567

        auth = OAuthAuthentication(
            expiry_margin=999,
            body={},
            client="client",
        )
        auth._token_expiration = 9999
        auth._access_token = "valid-access-token"

        expected = {
            "Authorization": "Bearer valid-access-token",
        }
        assert auth.get_headers() == expected
