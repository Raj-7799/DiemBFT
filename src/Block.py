from Quorum import QC

class Block:
    def __init__(self, author: int, round: int, payload: str, qc: QC, id: str):
        self.author=author
        self.round=round
        self.payload=payload
        self.qc = qc 
        self.id =id 
    
    def get_block_identity_object():
        pass
