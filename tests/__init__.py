from unittest.mock import Mock

from apiclient.request_strategies import BaseRequestStrategy

from nordigen import Client


def test_client(token="secret-token", request_strategy=Mock(spec=BaseRequestStrategy)):
    return Client(token=token, request_strategy=request_strategy)
