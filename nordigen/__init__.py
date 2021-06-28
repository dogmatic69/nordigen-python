from nordigen.client import AccountClient, AgreementsClient, AspspsClient, RequisitionsClient


def Client(token, request_strategy=None):
    def instance():
        return instance

    instance.aspsps = AspspsClient(token=token, request_strategy=request_strategy)
    instance.agreements = AgreementsClient(token=token, request_strategy=request_strategy)
    instance.account = AccountClient(token=token, request_strategy=request_strategy)
    instance.requisitions = RequisitionsClient(token=token, request_strategy=request_strategy)

    return instance
