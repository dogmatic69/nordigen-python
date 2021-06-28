import os
import pprint
import random
import string
from uuid import uuid4 as uuid

from flask import Flask
from pyngrok import ngrok

from nordigen import Client

# More complext example that will go through the account linking
# process and display account info / balance once authenticated


token = os.environ["NORDIGEN_TOKEN"]
port = os.environ.get("NORDIGEN_PORT", 9100)

# The bank id from the chosen bank (see aspsps endpoints)
bank = os.environ.get("NORDIGEN_BANK", "SEB_ESSESESS_PRIVATE")

client = Client(token=token)


def link_flow(redirect):
    # First create the requisition
    requisition = create_requisition(redirect=redirect, enduser_id=uuid(), reference=rand())

    # link the requisition to a bank, this will give a "sign in" url
    # the user should visit and authenticate at the bank
    link = create_link(id=requisition["id"], aspsp_id=bank)
    pr("To link your account visit: {}".format(link["initiate"]))

    # once the user visits the above link and signs in, they are
    # redirected back to the ngrok connection configured below
    # where the request can be handled. Not sure it's even needed
    # though.

    # After this, the flow continues in the handler where it
    # will get all available accounts and list the info / balance for
    # each account


def create_requisition(redirect, enduser_id, reference):
    if not enduser_id or not reference:
        raise Exception("Missing required values")

    return client.requisitions.create(
        **{
            "redirect": redirect,
            "reference": reference,
            "enduser_id": enduser_id,
            "agreements": [],  # not used as we are using default end-user agreement
        }
    )


def create_link(id, aspsp_id):
    return client.requisitions.initiate(id=id, aspsp_id=aspsp_id)


def get_accounts(id):
    return client.requisitions.by_id(id=id)


def account_info(id):
    return client.account.info(id=id)


def account_balance(id):
    return client.account.balances(id=id)


###############################################################################
#
# Code related to support the example
#
###############################################################################


def pr(data):
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(data)


def rand(size=12, chars=string.ascii_uppercase + string.digits):
    return "".join(random.choice(chars) for _ in range(size))


def start_ngrok():
    return ngrok.connect(port, "http")


def start_flask():
    app = Flask(__name__)

    @app.route("/")
    def handler():
        # not figured out a good way to maintain state, manually enter
        # the id from the requisition that has been authenticated
        accounts = get_accounts(id="...")
        pr(accounts)

        for account in accounts["accounts"]:
            info = account_info(id=account)
            pr(info)

            balance = account_balance(id=account)
            pr(balance)

        return "<p>Hello, World!</p>"

    app.run(debug=True, host="0.0.0.0", port=port)
    return app


def start():
    con = start_ngrok()
    link_flow(redirect=con.public_url)

    start_flask()


start()
