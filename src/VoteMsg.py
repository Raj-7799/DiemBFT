# VoteMsg
# vote_info; // A VoteInfo record
# ledger_commit_info; // Speculated ledger info
# high_commit_qc; // QC to synchronize on committed blocks
# sender ← u; // Added automatically when constructed
# signature ← sign u (ledger commit info); // Signed automatically when constructed

from crypto import Keys
class VoteMsg:

    def __init__(self,ledger_commit_info):
        self._vote_info=None
        self._ledger_commit_info=ledger_commit_info
        self._high_commit_qc=None
        self._sender=list()
        self._sender=0 # both are same need to revisit
        
        key=Keys(self.sender)
        self.signature=key.sign(self.ledger_commit_info) # to be implmented 
        

    @property
    def ledger_commit_info(self):
        return self._ledger_commit_info

    @property
    def high_commit_qc(self):
        return self._high_commit_qc
    
    @high_commit_qc.setter
    def high_commit_qc(self,high_commit_qc):
        self.high_commit_qc=high_commit_qc

    