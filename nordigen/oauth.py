from time import time

from apiclient.authentication_methods import BaseAuthenticationMethod


class OAuthAuthentication(BaseAuthenticationMethod):
    """Authentication using secret_id and secret_key."""

    _access_token = None
    _token_expiration = None
    _refresh_token = None
    _refresh_expiration = None

    def __init__(
        self,
        body,
        client,
        expiry_margin=10,
    ):
        """Initialize OAuthAuthentication."""
        self._client = client
        self._body = body
        self._expiry_margin = expiry_margin

    def get_headers(self):
        self.refresh_token()
        return {
            "Authorization": f"Bearer {self._access_token}",
        }

    def refresh_token(self):
        if self._token_expiration and self._token_expiration >= int(time()):
            return True

        if self._refresh_expiration and self._refresh_expiration >= int(time()):
            ret = self._client.refresh(refresh_token=self._refresh_token)
            self._access_token = ret.get("access")
            self._token_expiration = int(time()) + int(ret.get("access_expires")) - self._expiry_margin
            return True

        ret = self._client.token(**self._body)
        self._access_token = ret.get("access")
        self._refresh_token = ret.get("refresh")
        self._token_expiration = int(time()) + int(ret.get("access_expires")) - self._expiry_margin
        self._refresh_expiration = int(time()) + int(ret.get("refresh_expires")) - self._expiry_margin
