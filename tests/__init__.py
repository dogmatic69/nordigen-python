from unittest.mock import Mock

from apiclient.request_strategies import BaseRequestStrategy

from nordigen import Client


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
