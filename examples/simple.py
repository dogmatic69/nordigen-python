import os
import pprint

from nordigen import wrapper as Client

# Minimal example that fetches available banks on the Nordigen platform

token = os.environ["NORDIGEN_TOKEN"]


pp = pprint.PrettyPrinter(indent=4)


def pr(data):
    pp.pprint(data)


client = Client(token=token)

pr(client.aspsps.by_country("SE"))
