import urllib
import warnings

from apiclient import APIClient, JsonResponseHandler

DEFAULT_SCOPE = ["transactions", "balances", "details"]


def next_page_by_url(response, previous_page_url):
    """Paginate by response URL.

    To use, decorate method with `@paginated(by_url=next_page_by_url)`

    Args:
        response (dict): The API response
        previous_page_url ([type]): [description]

    Returns:
        str
    """
    return response["next"]


class NordigenClient(APIClient):
    def __init__(
        self,
        auth,
        scheme="https",
        host="bankaccountdata.gocardless.com",
        base="/api",
        request_strategy=None,
        version="v2",
    ):
        """Nordigen client base class.

        Args:
            token (str): The API token
            scheme (str, optional): Defaults to 'https'.
            host (str, optional): Defaults to 'bankaccountdata.gocardless.com'.
            base (str, optional): Defaults to '/api'.
            request_strategy (BaseRequestStrategy, optional): Request handler. Defaults to None.
        """
        self.request_strategy = request_strategy
        self.scheme = scheme
        self.host = host
        self.version = version

        version = f"/{version}" if version else ""
        self.base = f"{base}{version}"

        super(NordigenClient, self).__init__(
            authentication_method=auth,
            response_handler=JsonResponseHandler,
            request_strategy=request_strategy,
        )

    def is_v2(self):
        return self.version == "v2"

    def url(self, fragment, url_args={}):
        """Build API URL.

        Args:
            fragment (str): The endpoint to be built
            url_args (dict, optional): url args to be added. Defaults to {}.

        Returns:
            str
        """
        url_args = ("?" + urllib.parse.urlencode(url_args)) if url_args else ""
        return f"{self.scheme}://{self.host}{self.base}/{fragment}/{url_args}"


class AuthClient(NordigenClient):
    def token(self, secret_id, secret_key):
        url = self.url(fragment="token/new")
        return self.post(
            url,
            data={
                "secret_id": secret_id,
                "secret_key": secret_key,
            },
        )

    def refresh(self, refresh_token):
        url = self.url(fragment="token/refresh")
        return self.post(
            url,
            data={
                "refresh_token": refresh_token,
            },
        )


class AccountClient(NordigenClient):
    def info(self, id):
        url = self.url(fragment=f"accounts/{id}")
        return self.get(url)

    def balances(self, id):
        url = self.url(fragment=f"accounts/{id}/balances")
        return self.get(url)

    def details(self, id):
        url = self.url(fragment=f"accounts/{id}/details")
        return self.get(url)

    def transactions(self, id):
        url = self.url(fragment=f"accounts/{id}/transactions")
        return self.get(url)


class PremiumClient(NordigenClient):
    def balances(self, id):
        if not self.is_v2():
            raise NotImplementedError()

        url = self.url(fragment=f"accounts/premium/{id}/balances")
        return self.get(url)

    def details(self, id):
        if not self.is_v2():
            raise NotImplementedError()

        url = self.url(fragment=f"accounts/premium/{id}/details")
        return self.get(url)

    def transactions(self, id):
        if not self.is_v2():
            raise NotImplementedError()

        url = self.url(fragment=f"accounts/premium/{id}/transactions")
        return self.get(url)


class AgreementsClient(NordigenClient):
    endpoint = "agreements/enduser"

    def list(self, limit=None, offset=None):
        if not self.is_v2():
            raise NotImplementedError()

        url_args = dict(limit=limit, offset=offset)
        url_args = {k: v for k, v in url_args.items() if v}

        url = self.url(fragment=self.endpoint, url_args=url_args)
        return self.get(url)

    def _create_data_v2(self, aspsp_id, enduser_id, institution_id, access_scope, historical_days, access_days):
        if aspsp_id:
            warnings.warn("aspsp_id is deprecated in v2", DeprecationWarning)

        if enduser_id:
            raise ValueError("enduser_id is not required for v2")

        institution_id = institution_id or aspsp_id
        if not institution_id:
            raise ValueError("institution_id is required for v2")

        return {
            "max_historical_days": historical_days,
            "access_valid_for_days": access_days,
            "access_scope": access_scope,
            "institution_id": institution_id,
        }

    def create(
        self,
        enduser_id=None,
        aspsp_id=None,
        institution_id=None,
        historical_days=30,
        access_days=30,
        access_scope=DEFAULT_SCOPE,
    ):
        url = self.url(fragment=self.endpoint)

        if not aspsp_id and not self.is_v2():
            raise ValueError("aspsp_id is required for v1")

        if not enduser_id and not self.is_v2():
            raise ValueError("enduser_id is required for v1")

        data = {
            "max_historical_days": historical_days,
            "enduser_id": enduser_id,
            "aspsp_id": aspsp_id,
        }

        if self.is_v2():
            data = self._create_data_v2(
                aspsp_id=aspsp_id,
                enduser_id=enduser_id,
                institution_id=institution_id,
                access_scope=access_scope,
                historical_days=historical_days,
                access_days=access_days,
            )

        return self.post(url, data=data)

    def by_enduser_id(self, enduser_id, limit=None, offset=None):
        warnings.warn(
            "list by enduser_id is not supported in v2, fetch all with AgreementsClient().list()", DeprecationWarning
        )
        if self.is_v2():
            return self.list(limit=limit, offset=offset)

        url_args = dict(enduser_id=enduser_id, limit=limit, offset=offset)
        url_args = {k: v for k, v in url_args.items() if v}

        url = self.url(fragment=self.endpoint, url_args=url_args)
        return self.get(url)

    def by_id(self, id):
        url = self.url(fragment=f"{self.endpoint}/{id}")
        return self.get(url)

    def remove(self, id):
        url = self.url(fragment=f"{self.endpoint}/{id}")
        return self.delete(url)

    def accept(self, id):
        url = self.url(fragment=f"{self.endpoint}/{id}/accept")
        return self.put(url, {"user_agent": "user-agent", "ip_address": "127.0.0.1"})

    def text(self, id):
        warnings.warn("AgreementsClient().text() has been removed in V2", DeprecationWarning)
        if self.is_v2():
            raise NotImplementedError()

        url = self.url(fragment=f"{self.endpoint}/{id}/text")
        return self.get(url)


class InstitutionsClient(NordigenClient):
    def by_country(self, country):
        url = self.url(
            fragment="institutions",
            url_args={
                "country": country,
            },
        )
        return self.get(url)

    def by_id(self, id):
        url = self.url(fragment=f"institutions/{id}")
        return self.get(url)


class AspspsClient(NordigenClient):
    def by_country(self, country):
        warnings.warn("AspspsClient() has been replaced by InstitutionsClient() in V2", DeprecationWarning)
        url = self.url(
            fragment="aspsps" if not self.is_v2() else "institutions",
            url_args={
                "country": country,
            },
        )
        return self.get(url)

    def by_id(self, id):
        warnings.warn("AspspsClient() has been replaced by InstitutionsClient() in V2", DeprecationWarning)
        url = self.url(fragment=f"aspsps/{id}" if not self.is_v2() else f"institutions/{id}")
        return self.get(url)


class RequisitionsClient(NordigenClient):
    def list(self, limit=None, offset=None):
        url_args = dict(limit=limit, offset=offset)
        url_args = {k: v for k, v in url_args.items() if v}

        url = self.url(fragment="requisitions", url_args=url_args)
        return self.get(url)

    def by_id(self, id):
        url = self.url(fragment=f"requisitions/{id}")
        return self.get(url)

    def remove(self, id):
        url = self.url(fragment=f"requisitions/{id}")
        return self.delete(url)

    def create_v2(
        self, redirect, institution_id, reference, agreement=None, language=None, ssn=None, account_selection=False
    ):
        if not self.is_v2():
            raise NotImplementedError()

        url = self.url(fragment="requisitions")
        data = {
            "redirect": redirect,
            "institution_id": institution_id,
            "reference": reference,
            "account_selection": account_selection,
        }

        if agreement:
            data["agreement"] = agreement

        if language:
            data["user_language"] = language

        if ssn:
            data["ssn"] = ssn

        return self.post(url, data=data)

    def create(self, redirect, reference, enduser_id=None, agreements=[], language=None, **kwargs):
        warnings.warn("RequisitionsClient().create() has breaking changes in V2", DeprecationWarning)
        if self.is_v2():
            return self.create_v2(redirect=redirect, reference=reference, language=language, **kwargs)

        if not enduser_id:
            raise ValueError("enduser_id is required")

        url = self.url(fragment="requisitions")
        data = {
            "redirect": redirect,
            "agreements": agreements,
            "reference": reference,
            "enduser_id": enduser_id,
        }
        if language:
            data["user_language"] = language

        return self.post(url, data=data)

    def initiate(self, id, aspsp_id):
        if self.is_v2():
            raise NotImplementedError()

        url = self.url(fragment=f"requisitions/{id}/links")
        return self.post(
            url,
            {
                "aspsp_id": aspsp_id,
            },
        )
