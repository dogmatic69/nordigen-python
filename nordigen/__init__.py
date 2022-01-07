import warnings

from apiclient import HeaderAuthentication, NoAuthentication

from nordigen.client import (
    AccountClient,
    AgreementsClient,
    AspspsClient,
    AuthClient,
    InstitutionsClient,
    PremiumClient,
    RequisitionsClient,
)
from nordigen.oauth import OAuthAuthentication


def wrapper(token=None, request_strategy=None, secret_id=None, secret_key=None, version=None):
    if token:
        warnings.warn("Use Client(secret_id=xxx, secret_key=xxx) instead of token", DeprecationWarning)

    if not token and (not secret_id or not secret_key):
        raise ValueError("secret_id and secret_key must be provided")

    def instance():
        return instance

    auth = HeaderAuthentication(scheme="Token", token=token)
    if not token:
        version = "v2" if not version else version
        auth = OAuthAuthentication(
            body={
                "secret_id": secret_id,
                "secret_key": secret_key,
            },
            client=AuthClient(auth=NoAuthentication(), request_strategy=request_strategy, version=version),
        )

    instance.aspsps = AspspsClient(auth=auth, request_strategy=request_strategy, version=version)
    instance.agreements = AgreementsClient(auth=auth, request_strategy=request_strategy, version=version)
    instance.account = AccountClient(auth=auth, request_strategy=request_strategy, version=version)
    instance.institutions = InstitutionsClient(auth=auth, request_strategy=request_strategy, version=version)
    instance.premium = PremiumClient(auth=auth, request_strategy=request_strategy, version=version)
    instance.requisitions = RequisitionsClient(auth=auth, request_strategy=request_strategy, version=version)

    return instance
