import requests

"""helper function that accept the url and data and send them to the server
    make sure the address and payload are correct
"""


def send(address: str, payload: str):
    server_code = requests.post(address, data=payload)

    return server_code.text
