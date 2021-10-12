from marshmallow import fields, Schema
from marshmallow.decorators import post_load
from vote import VoteInfo, VoteMsg, vote_msg_schema
from blockchain import LedgerCommitInfo

class QCSchema(Schema):
    vote_info = fields.Nested(VoteInfo.VoteInfoSchema())
    ledger_commit_info = fields.Nested(LedgerCommitInfo.LedgerCommitInfoSchema())
    signatures = fields.List(fields.Nested(vote_msg_schema.VoteMsgSchema))
    author = fields.Int()

    @post_load
    def to_object(self, data, **kwargs):
        return QC(**data)
