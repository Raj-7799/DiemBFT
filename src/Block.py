from Quorum import QC
import Util

class Block:
    def __init__(self, author: int, round: int, payload: str, qc: QC, id: str):
        self.author=author
        self.round=round
        self.payload=payload
        self.qc = qc 
        self.id = Util.sign_object(self.get_block_identity_object())
    
    def get_block_identity_object(self):
        return [self.author, self.round, self.payload, self.qc.vote_info.id, self.qc.signatures]
