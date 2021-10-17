class Message:
    def __init__(self, payload: str, signature: str):
        self.payload = payload
        self.signature = signature