from unittest.mock import Mock

import pytest
from apiclient.request_strategies import BaseRequestStrategy

from nordigen import wrapper as Client


def test_client(
    token=None,
    request_strategy=Mock(spec=BaseRequestStrategy),
    secret_id="secret-id",
    secret_key="secret-key",
):
    args = dict(
        token=token,
        request_strategy=request_strategy,
        secret_id=secret_id,
        secret_key=secret_key,
    )
    return Client(**args)


def test_client_with_token(
    token="token",
    request_strategy=Mock(spec=BaseRequestStrategy),
):
    args = dict(
        token=token,
        request_strategy=request_strategy,
    )

    with pytest.deprecated_call() as records:
        ret = Client(**args)

    assert len(records) == 1
    expected = "Use Client(secret_id=xxx, secret_key=xxx) instead of token"
    assert records[0].message.args[0] == expected

    return ret
