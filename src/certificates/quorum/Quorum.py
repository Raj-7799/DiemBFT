from vote import VoteInfo as voteinfo
from blockchain import LedgerCommitInfo as ledgerCommitInfo
from crypto import Keys as keys



class QC():
    def __init__(self,author):
        self._vote_info=voteinfo.VoteInfo()
        self._ledger_commit_info = ledgerCommitInfo.LedgerCommitInfo()
        self._signatures = "test"
        self._author=author
        key=keys.Keys(self._author) ## find sender 
        self._signature=key.sign_message(self._signatures)
        

    
    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, author):
        self._author = author

    @property
    def ledger_commit_info(self):
        return self._ledger_commit_info
    
    @ledger_commit_info.setter
    def ledger_commit_info(self, ledger_commit_info):
        self._ledger_commit_info = ledger_commit_info

    @property
    def vote_info(self):
        return self._vote_info
    
    @vote_info.setter
    def vote_info(self, vote_info):
        self._vote_info = vote_info

    @property
    def signatures(self):
        return self._signatures
    
    @signatures.setter
    def signatures(self, signatures):
        self._signatures = signatures
