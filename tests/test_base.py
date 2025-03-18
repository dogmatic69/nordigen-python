import unittest

from apiclient import HeaderAuthentication

from nordigen.client import NordigenClient, next_page_by_url

header_auth = HeaderAuthentication(scheme="Token", token="fizz-buzz")


class TestBaseAuth(unittest.TestCase):
    def test_token_auth(self):
        client = NordigenClient(auth=header_auth)

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
        client = NordigenClient(auth=None, host="localhost")

        result = client.url("foo")
        self.assertEqual(result, "https://localhost/api/v2/foo/")

    def test_url_scheme(self):
        client = NordigenClient(auth=None, scheme="sftp")

        result = client.url("foo")
        self.assertEqual(result, "sftp://bankaccountdata.gocardless.com/api/v2/foo/")

    def test_url_base(self):
        client = NordigenClient(auth=None, base="")

        result = client.url("foo")
        self.assertEqual(result, "https://bankaccountdata.gocardless.com/v2/foo/")

        client = NordigenClient(auth=None, base="/some/thing/here")

        result = client.url("foo")
        self.assertEqual(result, "https://bankaccountdata.gocardless.com/some/thing/here/v2/foo/")

    def test_url_basic(self):
        client = NordigenClient(auth=None)

        result = client.url("foo")
        self.assertEqual(result, "https://bankaccountdata.gocardless.com/api/v2/foo/")

        result = client.url("foo/bar")
        self.assertEqual(result, "https://bankaccountdata.gocardless.com/api/v2/foo/bar/")

    def test_url_args(self):
        client = NordigenClient(auth=None)

        result = client.url("foo", url_args={})
        self.assertEqual(result, "https://bankaccountdata.gocardless.com/api/v2/foo/")

        result = client.url("foo", url_args={"fizz": "buzz"})
        self.assertEqual(result, "https://bankaccountdata.gocardless.com/api/v2/foo/?fizz=buzz")
