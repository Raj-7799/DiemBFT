from marshmallow import fields
from marshmallow.decorators import post_load
import VoteInfo
import LedgerCommitInfo
import Keys as keys
import Util

class QC():
    def __init__(self,vote_info,ledger_commit_info,votes=None):
        self.vote_info=vote_info
        self.ledger_commit_info = ledger_commit_info
        self.signatures=votes
        self.author=0
        key=keys.Keys(self.author) ## find sender 
        self._signature=key.sign_message(self.signatures)
