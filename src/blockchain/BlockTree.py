import nacl.hash
from quorum import Quorum
import Block as block
class BlockTree:
    def __init__(self):
        self._qc = Quorum.QC(1)
        self._high_qc = Quorum.QC(1) # highest known QC
        self._pending_votes=None # collected votes per block indexed by their LedgerInfo hash
        self._high_commit_qc=Quorum.QC(1) # highest QC that serves as a commit certificate
        
    @property
    def qc(self):
        return self._qc

    @property
    def high_qc(self):
        return self._high_qc
    
    @property
    def pending_votes(self):
        return self._pending_votes
    
    @property
    def high_commit_qc(self):
        return self._high_commit_qc

    def process_qc(self,qc):
        pass
    

    def execute_insert(self,block):
        pass
    
    def process_vote(self,vote):
        pass

    def generate_block(self,txns,current_round):
        author=0
        HASHER = nacl.hash.sha256
        msg =  str.encode(str(author)+str(current_round)+str(self.qc.vote_info.id)+str(self.qc.signature))
        id = HASHER(msg, encoder=nacl.encoding.HexEncoder)

        new_block = block.Block(author=author,round=current_round,payload=txns,qc=self.high_qc,id=id)
        return new_block
        
    

x=BlockTree()
compute_block=x.generate_block(1,2)
print(compute_block)