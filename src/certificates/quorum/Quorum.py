import VoteInfo as voteInfo
import LedgerCommitInfo as ledgerCommitInfo

class QC():
    def __init__(self,author):
        self._vote_info=voteInfo.VoteInfo()
        self._ledger_commit_info = ledgerCommitInfo.LedgerCommitInfo()
        self._signature=None
        self._author=author

    
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
    def signature(self):
        return self._signature
