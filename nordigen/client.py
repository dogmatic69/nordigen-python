import urllib

from apiclient import APIClient, HeaderAuthentication, JsonResponseHandler


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
    def __init__(self, token, scheme='https', host='ob.nordigen.com', base='/api', request_strategy=None):
        """Nordigen client base class.

        Args:
            token (str): The API token
            scheme (str, optional): Defaults to 'https'.
            host (str, optional): Defaults to 'ob.nordigen.com'.
            base (str, optional): Defaults to '/api'.
            request_strategy (BaseRequestStrategy, optional): Request handler. Defaults to None.
        """
        self.request_strategy = request_strategy
        self.scheme = scheme
        self.host = host
        self.base = base

        super(NordigenClient, self).__init__(
            authentication_method=HeaderAuthentication(scheme='Token', token=token),
            response_handler=JsonResponseHandler,
            request_strategy=request_strategy,
        )

    def url(self, fragment, url_args={}):
        """Build API URL.

        Args:
            fragment (str): The endpoint to be built
            url_args (dict, optional): url args to be added. Defaults to {}.

        Returns:
            str
        """
        url_args = ('?' + urllib.parse.urlencode(url_args)) if url_args else ''
        return f'{self.scheme}://{self.host}{self.base}/{fragment}/{url_args}'


class AccountClient(NordigenClient):
    def info(self, id):
        url = self.url(fragment=f'accounts/{id}')
        return self.get(url)

    def balances(self, id):
        url = self.url(fragment=f'accounts/{id}/balances')
        return self.get(url)

    def details(self, id):
        url = self.url(fragment=f'accounts/{id}/details')
        return self.get(url)

    def transactions(self, id):
        url = self.url(fragment=f'accounts/{id}/transactions')
        return self.get(url)


class AgreementsClient(NordigenClient):
    def create(self, enduser_id, aspsp_id, historical_days=30):
        url = self.url(fragment='agreements/enduser')
        return self.post(url, data={
            "max_historical_days": historical_days,
            "enduser_id": enduser_id,
            "aspsp_id": aspsp_id,
        })

    def by_enduser_id(self, enduser_id, limit=None, offset=None):
        url_args = dict(enduser_id=enduser_id, limit=limit, offset=offset)
        url_args = {k: v for k, v in url_args.items() if v}

        url = self.url(fragment='agreements/enduser', url_args=url_args)
        return self.get(url)

    def by_id(self, id):
        url = self.url(fragment=f'agreements/enduser/{id}')
        return self.get(url)

    def remove(self, id):
        url = self.url(fragment=f'agreements/enduser/{id}')
        return self.delete(url)

    def accept(self, id):
        url = self.url(fragment=f'agreements/enduser/{id}/accept')
        return self.put(url, {
            "user_agent": "user-agent",
            "ip_address": "127.0.0.1"
        })

    def text(self, id):
        url = self.url(fragment=f'agreements/enduser/{id}/text')
        return self.get(url)


class AspspsClient(NordigenClient):
    def by_country(self, country):
        url = self.url(fragment='aspsps', url_args={
            'country': country,
        })
        return self.get(url)

    def by_id(self, id):
        url = self.url(fragment=f'aspsps/{id}')
        return self.get(url)


class RequisitionsClient(NordigenClient):
    def list(self, limit=None, offset=None):
        url_args = dict(limit=limit, offset=offset)
        url_args = {k: v for k, v in url_args.items() if v}

        url = self.url(fragment='requisitions', url_args=url_args)
        return self.get(url)

    def by_id(self, id):
        url = self.url(fragment=f'requisitions/{id}')
        return self.get(url)

    def remove(self, id):
        url = self.url(fragment=f'requisitions/{id}')
        return self.delete(url)

    def create(self, redirect, enduser_id, reference, agreements=[], language=None):
        url = self.url(fragment='requisitions')
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
        url = self.url(fragment=f'requisitions/{id}/links')
        return self.post(url, {
            "aspsp_id": aspsp_id,
        })
