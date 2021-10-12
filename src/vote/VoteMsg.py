# VoteMsg
# vote_info; // A VoteInfo record
# ledger_commit_info; // Speculated ledger info
# high_commit_qc; // QC to synchronize on committed blocks
# sender ← u; // Added automatically when constructed
# signature ← sign u (ledger commit info); // Signed automatically when constructed

from marshmallow.decorators import post_load
from crypto import Keys as keys
from marshmallow import Schema, fields
from .VoteInfo import VoteInfoSchema
from blockchain import LedgerCommitInfo as lci
from certificates.quorum.quorum_schema import QCSchema
from util import Util

class VoteMsg:

    def __init__(self,vote_info,ledger_commit_info, high_commit_qc, sender):
        self.vote_info = vote_info
        self.ledger_commit_info = ledger_commit_info
        self.high_commit_qc = high_commit_qc
        #self._sender=list()
        self.sender = sender # both are same need to revisit
        
        key=keys.Keys(self.sender) ## find sender 
        # Using digtal signature to sign the message to avoid computation for generating message using public-private key encryption
        self.signature=key.sign_message(Util.serialize(self.ledger_commit_info, self.ledger_commit_info.schema))

    # @property
    # def sender(self):
    #     return self._sender

    # @property
    # def signature(self):
    #     return self._signature

    # @property
    # def ledger_commit_info(self):
    #     return self._ledger_commit_info

    # @property
    # def high_commit_qc(self):
    #     return self._high_commit_qc
    
    # @high_commit_qc.setter
    # def high_commit_qc(self,high_commit_qc):
    #     self.high_commit_qc=high_commit_qc

class VoteMsgSchema(Schema):
    vote_info = fields.Nested(VoteInfoSchema)
    ledger_commit_info = fields.Nested(lci.LedgerCommitInfoSchema)
    high_commit_qc = fields.Nested(QCSchema)
    sender = fields.Int()

    @post_load
    def to_object(self, data, **kwargs):
        return VoteMsg(**data)
