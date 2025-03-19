import os
import sys
import unittest
from uuid import uuid4 as uuid

import pytest
from bs4 import BeautifulSoup
from requests_html import HTMLSession

from nordigen import wrapper as Client

secret_id = os.environ.get("NORDIGEN_SANDBOX_SECRET_ID")
secret_key = os.environ.get("NORDIGEN_SANDBOX_SECRET_KEY")

missing_secret = secret_id is None or secret_key is None
py39 = sys.version_info.major == 3 and sys.version_info.minor == 9
pytestmark = pytest.mark.skipif(
    missing_secret or not py39, reason="No credentials provided or not running due to conflicts"
)


def client():
    return Client(secret_id=secret_id, secret_key=secret_key)


@pytest.mark.order("second_to_last")
class TestIntegrationBasics(unittest.TestCase):
    def test_have_credentials(self):
        assert secret_id
        assert secret_key

    def test_cleanup_requisitions(self):
        c = client()

        response = c.requisitions.list()
        for requisition in response.get("results", []):
            try:
                c.requisitions.remove(requisition["id"])
            except Exception:
                len(requisition["id"])

    @pytest.mark.order(after="TestIntegrationBasics::test_cleanup_requisitions")
    def test_cleanup_agreements(self):
        c = client()

        response = c.agreements.list()
        for agreement in response.get("results", []):
            try:
                c.agreements.remove(agreement["id"])
            except Exception:
                len(agreement["id"])


@pytest.mark.order("second_to_last")
class TestIntegrationInstitutions(unittest.TestCase):
    def test_institutions_by_country(self):
        c = client()

        response = c.institutions.by_country("SE")
        assert "SEB_ESSESESS_PRIVATE" in [i["id"] for i in response]

        response = c.institutions.by_country("GB")
        assert "BANK_OF_IRELAND_B365_BOFIGB2B" in [i["id"] for i in response]

    def test_institution_by_id(self):
        c = client()

        response = c.institutions.by_id("SEB_ESSESESS_PRIVATE")
        assert response == {
            "id": "SEB_ESSESESS_PRIVATE",
            "name": "SEB Private",
            "bic": "ESSESESS",
            "transaction_total_days": "730",
            "countries": ["SE"],
            "logo": "https://cdn.nordigen.com/ais/SEB_ESSESESS_PRIVATE.png",
        }


@pytest.mark.order("second_to_last")
class TestIntegrationAgreements(unittest.TestCase):
    def test_create_agreement(self):
        c = client()

        response = c.agreements.create(
            institution_id="SANDBOXFINANCE_SFIN0000",
            historical_days=43,
            access_days=34,
        )
        self.assertEqual(response["institution_id"], "SANDBOXFINANCE_SFIN0000")

    @pytest.mark.order(after="TestIntegrationAgreements::test_create_agreement")
    def test_get_agreement_by_id(self):
        c = client()
        response = c.agreements.list()
        id = next(
            agreement["id"] for agreement in response.get("results", []) if agreement["max_historical_days"] == 43
        )

        self.assertTrue(id)
        result = c.agreements.by_id(id)

        self.assertEqual(len(result["id"]), 36)
        self.assertTrue(result["created"])
        self.assertEqual(result["max_historical_days"], 43)
        self.assertEqual(result["access_valid_for_days"], 34)
        self.assertEqual(result["access_scope"], ["balances", "details", "transactions"])
        self.assertIsNone(result["accepted"])
        self.assertEqual(result["institution_id"], "SANDBOXFINANCE_SFIN0000")

    @pytest.mark.order(after="TestIntegrationAgreements::test_get_agreement_by_id")
    def test_agreements_delete_all(self):
        c = client()

        response = c.agreements.list()
        for agreement in response.get("results", []):
            try:
                c.agreements.remove(agreement["id"])
            except Exception:
                len(agreement["id"])

        if len(response.get("results", [])):
            response = c.agreements.list()
            self.assertEqual(len(response.get("results", [])), 0)

    @pytest.mark.order(after="TestIntegrationAgreements::test_agreements_delete_all")
    def test_agreements_list(self):
        c = client()

        response = c.agreements.list()
        self.assertEqual(len(response.get("results", [])), 0)


@pytest.mark.order("second_to_last")
class TestIntegrationRequisitions(unittest.TestCase):
    reference = uuid()

    def test_create_requisition(self):
        c = client()

        with self.assertWarns(DeprecationWarning):
            response = c.requisitions.create(
                redirect="https://example.com/redirect",
                institution_id="SANDBOXFINANCE_SFIN0000",
                reference=self.reference,
            )

        self.assertEqual(len(response["id"]), 36)
        self.assertTrue(response["created"])
        self.assertEqual(response["redirect"], "https://example.com/redirect")
        self.assertEqual(response["institution_id"], "SANDBOXFINANCE_SFIN0000")
        self.assertEqual(response["reference"], str(self.reference))
        self.assertEqual(response["status"], "CR")
        self.assertEqual(response["accounts"], [])
        self.assertEqual(
            response["link"],
            f"https://bankaccountdata.gocardless.com/psd2/start/{response['id']}/SANDBOXFINANCE_SFIN0000",
        )
        self.assertIsNone(response["ssn"])

    def test_requisition_by_id(self):
        c = client()

        response = c.requisitions.list()
        id = next(
            requisition["id"]
            for requisition in response.get("results", [])
            if requisition["reference"] == str(self.reference)
        )

        self.assertTrue(id)
        result = c.requisitions.by_id(id)

        self.assertEqual(len(result["id"]), 36)
        self.assertEqual(result["redirect"], "https://example.com/redirect")
        self.assertEqual(result["institution_id"], "SANDBOXFINANCE_SFIN0000")
        self.assertEqual(result["reference"], str(self.reference))

    def test_requisition_delete_all(self):
        c = client()

        response = c.requisitions.list()
        for requisition in response.get("results", []):
            try:
                c.requisitions.remove(requisition["id"])
            except Exception:
                len(requisition["id"])

        if len(response.get("results", [])):
            response = c.requisitions.list()
            self.assertEqual(len(response.get("results", [])), 0)

    @pytest.mark.order(after="TestIntegrationAgreements::test_agreements_delete_all")
    def test_requisitions(self):
        c = client()

        response = c.requisitions.list()
        assert response["count"] == 0
        assert response["results"] == []


@pytest.mark.order("last")
class TestIntegrationFullFlow(unittest.TestCase):
    session = HTMLSession()

    def get_page_as_soup(self, url):
        res = self.session.get(url)
        res.html.render()
        return BeautifulSoup(res.content, "html.parser")

    def get_form(self, url, index=0):
        soup = self.get_page_as_soup(url)
        forms = soup.find_all("form")

        return forms[index]

    def form_details(self, form, url=None):
        return {
            "action": f"{url}{form.attrs.get('action')}",
            "method": form.attrs.get("method", "get").lower(),
            "inputs": [
                {
                    "type": input.attrs.get("type", "text"),
                    "name": input.attrs.get("name"),
                    "value": input.attrs.get("value", ""),
                }
                for input in form.find_all("input")
            ],
        }

    def submit_form(self, url, method, inputs, extra_data={}, referer=None):
        data = {data["name"]: data["value"] for data in inputs if data["type"] == "hidden"}
        data = {**data, **extra_data}

        fn = getattr(self.session, method)
        args = {"data": data} if method == "post" else {"params": data}
        args["headers"] = dict(Referer=(referer or url))

        return fn(url, **args)

    def test_full_flow(self):
        """Full flow of the integration test.

        This method tests the entire flow from creating a connection to a bank
        through authorization to getting the account details and transactions.
        """
        c = client()

        with self.assertWarns(DeprecationWarning):
            # 1a. Create a new requisition
            result = c.requisitions.create(
                redirect="https://example.com/redirect",
                institution_id="SANDBOXFINANCE_SFIN0000",
                reference=uuid(),
            )
            self.assertEqual(result["status"], "CR")  # Requisition is not yet linked
            requisition_id = result["id"]

        with self.assertWarns(DeprecationWarning):
            self.assertEqual(len(result["id"]), 36)

            # 2a. Load the requisition link page
            form = self.get_form(result["link"], 1)

            # 2b. Click accept to start the flow
            details = self.form_details(form, result["link"])
            res = self.submit_form(
                url=result["link"],
                inputs=details["inputs"],
                method=details["method"],
            )

            # 3a. Follow the redirect to the sandbox banking site
            soup = BeautifulSoup(res.content, "html.parser")
            meta = next(a for a in soup.find_all("meta") if a.attrs.get("http-equiv", "") == "refresh")
            sandbox_url = meta.attrs.get("content").split(";")[-1].split("url=")[-1]

            # 3b. Load the login page
            form = self.get_form(sandbox_url, 0)
            details = self.form_details(form, url="https://sandboxfinance.nordigen.com")

            # 3c. Submit the login form
            res = self.submit_form(
                url=details["action"],
                referer=sandbox_url,
                inputs=details["inputs"],
                method=details["method"],
                extra_data={
                    "username": "test",
                    "password": "test",
                },
            )

            # 4a. Click accept on the sandbox banking site to approve the connection
            soup = BeautifulSoup(res.content, "html.parser")
            accept_link = soup.find_all("a")[0].attrs.get("href")
            soup = self.get_page_as_soup(accept_link)

            self.assertEqual(soup.find_all("h1")[0].text, "Example Domain")

            # 5a. List accounts
            result = c.requisitions.by_id(requisition_id)
            account_id = result["accounts"][0]

            self.assertEqual(result["status"], "LN")  # Requisition is now linked
            self.assertGreater(len(result["accounts"]), 0)

            # 5b. Fetch account details and transactions
            result = c.account.info(account_id)
            self.assertEqual(result["status"], "READY")

            result = c.account.balances(account_id)
            self.assertEqual(len(result["balances"]), 2)
            self.assertGreater(float(result["balances"][0]["balanceAmount"]["amount"]), 0)

            result = c.account.details(account_id)
            self.assertGreater(len(result["account"]["ownerName"]), 0)
            self.assertEqual(len(result["account"]["iban"]), 19)

            result = c.account.transactions(account_id)
            self.assertGreater(len(result["transactions"]["booked"]), 10)
            self.assertTrue(result["transactions"]["booked"][0]["transactionAmount"]["amount"])
            self.assertEqual(len(result["transactions"]["booked"][0]["transactionAmount"]["currency"]), 3)
