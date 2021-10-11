from vote import VoteInfo as voteinfo
from blockchain import LedgerCommitInfo as ledgerCommitInfo
from crypto import Keys as keys



class QC():
    def __init__(self,vote_info,ledger_commit_info,votes):
        self._vote_info=vote_info
        self._ledger_commit_info = ledger_commit_info
        self._signatures=votes
        self._author=0
        key=keys.Keys(self._author) ## find sender 
        self._signature=key.sign_message(self._signatures)
        

    
    @property
    def author(self):
        return self._author

    @property
    def ledger_commit_info(self):
        return self._ledger_commit_info
    
    @property
    def vote_info(self):
        return self._vote_info
    

    @property
    def signatures(self):
        return self._signatures
