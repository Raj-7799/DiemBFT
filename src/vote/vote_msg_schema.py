from .VoteInfo import VoteInfoSchema
from blockchain import LedgerCommitInfo as lci
from certificates.quorum.quorum_schema import QCSchema
from marshmallow import Schema, fields
from marshmallow.decorators import post_load
from .VoteMsg import VoteMsg

class VoteMsgSchema(Schema):
    vote_info = fields.Nested(VoteInfoSchema)
    ledger_commit_info = fields.Nested(lci.LedgerCommitInfoSchema)
    high_commit_qc = fields.Nested(QCSchema)
    sender = fields.Int()

    @post_load
    def to_object(self, data, **kwargs):
        return VoteMsg(**data)