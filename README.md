# Nordigen API Client

Nordigen is a (always*) free banking API that takes advantage of the EU PSD2
regulations. They connect to banks in over 30 countries using real banking
API's (no screen scraping).

Nordigen's API is an abstraction over the usual bank API's so that all data
is in a consistent format. They also handle all the regulations required to
get access to the data.

The client is built using the python [api-client](https://github.com/MikeWooster/api-client) lib.

I found this info thanks to this site: https://www.bankapi.se/

_\* According to Nordigen's own website :)_

## Nordigen Info

- Sales pitch: https://nordigen.com/en/products/account-information/
- Docs: https://nordigen.com/en/account_information_documenation/api-documention/overview/
- API Spec: https://ob.nordigen.com/api/docs

## Installation

```
pip install nordigen-python
```

## Usage

Some more indepth working examples can be found in `./examples`. Also check out the test cases for usage examples.

Create a client instance

```
from nordigen import Client

client = Client(token="super-secret-token")
```

Listing available banks

```
banks = client.aspsps.by_country('SE')
print(banks)

# [
#   {
#     "id": "ABNAMRO_FTSBDEFAXXX",
#     "name": "ABN AMRO Bank Commercial",
#     "bic": "FTSBDEFAXXX",
#     "transaction_total_days": "558",
#     "countries": [
#       "DE"
#     ]
#   },
#   {
#     "id": "AACHENER_BANK_GENODED1AAC",
#     "name": "Aachener Bank",
#     "bic": "GENODED1AAC",
#     "transaction_total_days": "400",
#     "countries": [
#       "DE"
#     ]
#   },
#   ...
# ]
```

Fetching the balance of your account:

```
balance = client.account.balances("account-id")
print(balance)

# {
#   "balances": [
#     {
#       "balanceAmount": {
#         "amount": "-207.41",
#         "currency": "GBP"
#       },
#       "balanceType": "string",
#       "referenceDate": "2021-06-24"
#     },
#     {
#       "balanceAmount": {
#         "amount": "-649.63",
#         "currency": "GBP"
#       },
#       "balanceType": "string",
#       "referenceDate": "2021-06-21"
#     }
#   ]
# }
```

