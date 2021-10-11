# VoteMsg
# vote_info; // A VoteInfo record
# ledger_commit_info; // Speculated ledger info
# high_commit_qc; // QC to synchronize on committed blocks
# sender ← u; // Added automatically when constructed
# signature ← sign u (ledger commit info); // Signed automatically when constructed

from crypto import Keys as keys

class VoteMsg:

    def __init__(self, u):
        self._vote_info = None
        self._ledger_commit_info = None
        self._high_commit_qc = None
        self._sender=u # both are same need to revisit
        
        key=keys.Keys(self.sender) ## find sender 
        # Using digtal signature to sign the message to avoid computation for generating message using public-private key encryption
        self._signature=key.sign_message(self._ledger_commit_info) 
        

    @property
    def vote_info(self):
        return self._vote_info

    @vote_info.setter
    def sender(self, vote_info):
        self._vote_info = vote_info
    
    @property
    def sender(self):   
        return self._sender

    @sender.setter
    def sender(self, sender):
        self._sender = sender

    @property
    def signature(self):
        return self._signature

    @signature.setter
    def signature(self, signature):
        self._signature = signature

    @property
    def ledger_commit_info(self):
        return self._ledger_commit_info

    @ledger_commit_info.setter
    def ledger_commit_info(self, ledger_commit_info):
        self._ledger_commit_info = ledger_commit_info

    @property
    def high_commit_qc(self):
        return self._high_commit_qc
    
    @high_commit_qc.setter
    def high_commit_qc(self, high_commit_qc):
        self._high_commit_qc = high_commit_qc

    