import unittest
from unittest.mock import Mock

from apiclient.request_strategies import BaseRequestStrategy

from nordigen import Client
from nordigen.client import NordigenClient


class TestClient(unittest.TestCase):
    def test_basic(self):
        client = Client(token="whoo", request_strategy=Mock(spec=BaseRequestStrategy))

        self.assertEqual(client, client())

    def test_instances(self):
        client = Client(token="whoo", request_strategy=Mock(spec=BaseRequestStrategy))
        self.assertIsInstance(client.aspsps, NordigenClient)
        self.assertIsInstance(client.agreements, NordigenClient)
        self.assertIsInstance(client.account, NordigenClient)
        self.assertIsInstance(client.requisitions, NordigenClient)
