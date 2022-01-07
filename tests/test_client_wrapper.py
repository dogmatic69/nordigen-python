import unittest
from unittest.mock import Mock

from apiclient.request_strategies import BaseRequestStrategy

from nordigen import wrapper as Client
from nordigen.client import NordigenClient


class TestClient(unittest.TestCase):
    def test_basic(self):
        client = Client(secret_id="secret", secret_key="secret", request_strategy=Mock(spec=BaseRequestStrategy))

        self.assertEqual(client, client())

    def test_instances(self):
        client = Client(secret_id="secret", secret_key="secret", request_strategy=Mock(spec=BaseRequestStrategy))
        self.assertIsInstance(client.aspsps, NordigenClient)
        self.assertIsInstance(client.agreements, NordigenClient)
        self.assertIsInstance(client.account, NordigenClient)
        self.assertIsInstance(client.requisitions, NordigenClient)

    def test_pool(self):
        client = Client(secret_id="secret", secret_key="secret", request_strategy=Mock(spec=BaseRequestStrategy))
        self.assertIsInstance(client.aspsps, NordigenClient)

    def test_warning_for_depreciated_config(self):
        with self.assertWarns(DeprecationWarning):
            Client(token="token")

    def test_exception_missing_secret_id(self):
        with self.assertRaises(ValueError):
            Client(secret_key="secret")

    def test_exception_missing_secret_key(self):
        with self.assertRaises(ValueError):
            Client(secret_id="secret")

    def test_exception_missing_secret_id_and_secret_key(self):
        with self.assertRaises(ValueError):
            Client()
