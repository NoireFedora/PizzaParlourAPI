import requests

"""helper function that accept the url and data and send them to the server
    make sure the address and payload are correct
"""


def post(address: str, payload: str):
    server_code = requests.post(address, data=payload)
    return server_code


def delete(address: str, payload: str):
    server_code = requests.delete(address, data=payload)
    return server_code


def get(address: str, payload: str):
    server_code = requests.get(address, data=payload)
    return server_code
