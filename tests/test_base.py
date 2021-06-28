import unittest

from nordigen.client import NordigenClient as Client
from nordigen.client import next_page_by_url


class TestBaseAuth(unittest.TestCase):
    def test_token(self):
        client = Client(token="fizz-buzz")

        self.assertEqual(
            client.get_default_headers(),
            {
                "Authorization": "Token fizz-buzz",
            },
        )


class TestBasePagination(unittest.TestCase):
    def test_pagination(self):
        result = next_page_by_url({"next": "http://example.com/page/2"}, None)
        self.assertEqual(result, "http://example.com/page/2")


class TestBaseUrl(unittest.TestCase):
    def test_url_host(self):
        client = Client(token="asdf", host="localhost")

        result = client.url("foo")
        self.assertEqual(result, "https://localhost/api/foo/")

    def test_url_scheme(self):
        client = Client(token="asdf", scheme="http")

        result = client.url("foo")
        self.assertEqual(result, "http://ob.nordigen.com/api/foo/")

    def test_url_base(self):
        client = Client(token="asdf", base="")

        result = client.url("foo")
        self.assertEqual(result, "https://ob.nordigen.com/foo/")

        client = Client(token="asdf", base="/some/thing/here")

        result = client.url("foo")
        self.assertEqual(result, "https://ob.nordigen.com/some/thing/here/foo/")

    def test_url_basic(self):
        client = Client(token="asdf")

        result = client.url("foo")
        self.assertEqual(result, "https://ob.nordigen.com/api/foo/")

        result = client.url("foo/bar")
        self.assertEqual(result, "https://ob.nordigen.com/api/foo/bar/")

    def test_url_args(self):
        client = Client(token="asdf")

        result = client.url("foo", url_args={})
        self.assertEqual(result, "https://ob.nordigen.com/api/foo/")

        result = client.url("foo", url_args={"fizz": "buzz"})
        self.assertEqual(result, "https://ob.nordigen.com/api/foo/?fizz=buzz")
