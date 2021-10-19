import os

# Object to hold the info of the client as well as it's public key
class ClientInfo:
    def __init__(self, public_key: str, clientID: int):
        self.public_key = public_key
        self.clientID = clientID