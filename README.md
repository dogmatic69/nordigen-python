# Nordigen API Client

## Overview
[![GitHub](https://img.shields.io/github/license/dogmatic69/nordigen-python)](LICENSE.txt)
![Nordigen Quality](https://img.shields.io/badge/quality-high-green.svg)
[![Documentation Status](https://readthedocs.org/projects/nordigen-homeassistant/badge/?version=latest)](https://nordigen-homeassistant.readthedocs.io/en/latest/?badge=latest)

## Automation
[![CI](https://github.com/dogmatic69/nordigen-python/actions/workflows/ci.yaml/badge.svg)](https://github.com/dogmatic69/nordigen-python/actions/workflows/ci.yaml)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=dogmatic69_nordigen-python&metric=coverage)](https://sonarcloud.io/summary/new_code?id=dogmatic69_nordigen-python)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=dogmatic69_nordigen-python&metric=alert_status)](https://sonarcloud.io/dashboard?id=dogmatic69_nordigen-python)

## Security
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=dogmatic69_nordigen-python&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=dogmatic69_nordigen-python)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=dogmatic69_nordigen-python&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id=dogmatic69_nordigen-python)

## Quality
[![CodeFactor](https://www.codefactor.io/repository/github/dogmatic69/nordigen-python/badge)](https://www.codefactor.io/repository/github/dogmatic69/nordigen-python)
[![Duplicated Lines (%)](https://sonarcloud.io/api/project_badges/measure?project=dogmatic69_nordigen-python&metric=duplicated_lines_density)](https://sonarcloud.io/summary/new_code?id=dogmatic69_nordigen-python)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=dogmatic69_nordigen-python&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=dogmatic69_nordigen-python)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=dogmatic69_nordigen-python&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=dogmatic69_nordigen-python)
[![Technical Debt](https://sonarcloud.io/api/project_badges/measure?project=dogmatic69_nordigen-python&metric=sqale_index)](https://sonarcloud.io/summary/new_code?id=dogmatic69_nordigen-python)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=dogmatic69_nordigen-python&metric=bugs)](https://sonarcloud.io/summary/new_code?id=dogmatic69_nordigen-python)
[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=dogmatic69_nordigen-python&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=dogmatic69_nordigen-python)

## Compatibility
[![PyPi](https://img.shields.io/pypi/v/nordigen-python.svg)](https://pypi.python.org/pypi/nordigen-python/)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)

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

Note:  Nordigen was purchased by GoCardless in 2022. The API is still free to use, but
the company is now called GoCardless. The API is still the same, but the branding has changed.

- Sales pitch: https://nordigen.com/en/products/account-information/
- Docs: https://nordigen.com/en/account_information_documenation/api-documention/overview/
- API Spec: https://bankaccountdata.gocardless.com/api/docs
- OpenAPI Specification: https://bankaccountdata.gocardless.com/api/swagger.json

## Installation

```
pip install nordigen-python
```

## Usage

Some more in-depth working examples can be found in `./examples`. Also check out the test cases for usage examples.

Create a client instance

```
from nordigen import wrapper

client = wrapper(token="super-secret-token")
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

