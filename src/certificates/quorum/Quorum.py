from vote import VoteInfo, VoteMsg
from blockchain import LedgerCommitInfo
from crypto import Keys as keys
from util import Util

class QC():
    def __init__(self,vote_info,ledger_commit_info, votes=None):
        self.vote_info=vote_info
        self.ledger_commit_info = ledger_commit_info
        self.signatures=votes
        self.author=0
        key=keys.Keys(self.author) ## find sender 
        self.signature=key.sign_message(self.signatures)
    
    # @property
    # def author(self):
    #     return self._author

    # @property
    # def ledger_commit_info(self):
    #     return self._ledger_commit_info
    
    # @property
    # def vote_info(self):
    #     return self._vote_info
    

    # @property
    # def signatures(self):
    #     return self._signatures
