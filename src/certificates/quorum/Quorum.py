from marshmallow import fields
from marshmallow.decorators import post_load
from vote import VoteInfo
from blockchain import LedgerCommitInfo
from crypto import Keys as keys
from util import Util

class QC():
    def __init__(self,vote_info,ledger_commit_info,votes=None):
        self.vote_info=vote_info
        self.ledger_commit_info = ledger_commit_info
        self.signatures=votes
        self.author=0
        key=keys.Keys(self._author) ## find sender 
        self._signature=key.sign_message(self._signatures)
    
    # @property
    # def author(self):
    #     return self._author

    # @property
    # def ledger_commit_info(self):
    #     return self._ledger_commit_info
    
    # @property
    # def vote_info(self):
    #     return self._vote_info
    
    @vote_info.setter
    def vote_info(self, vote_info):
        self._vote_info = vote_info

    # @property
    # def signatures(self):
    #     return self._signatures

def QCSchema():
    vote_info = fields.Nested(VoteInfo.VoteInfoSchema())
    ledger_commit_info = fields.Nested(LedgerCommitInfo.LedgerCommitInfoSchema())
    signatures = fields.List(fields.Nested(VoteInfo.Vo))

    @post_load
    def to_object(self, data, **kwargs):
        return QC(**data)
