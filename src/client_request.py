import Util

# Class to hold client request that serves as transaction
class ClientRequest:
    def __init__(self, payload, source, pvt_key):
        self.payload = payload
        self.source = source
        self.signature = Util.sign_object_dup(self.payload, pvt_key)
    
    def __str__(self):
        return self.payload
    
    def __eq__(self, other):
        return other.signature == self.signature
    
    def __hash__(self) -> int:
        return self.payload.__hash__()
    
    def __lt__(self, other):
        return self.payload < other.payload