
# // speculated new committed state to vote directly on
# LedgerCommitInfo
# commit state id; // ⊥ if no commit happens when this vote is aggregated to QC
# vote info hash; // Hash of VoteMsg.vote info
from marshmallow import Schema, fields
from marshmallow.decorators import post_load


class LedgerCommitInfo:
    def __init__(self,commit_state_id=None,vote_info_hash=None):
        self.commit_state_id=commit_state_id
        self.vote_info_hash=vote_info_hash
    
    # @property
    # def commit_state_id(self):
    #     return self._commit_state_id

    # @property
    # def vote_info_hash(self):
    #     return self._vote_info_hash

    # @vote_info_hash.setter
    # def vote_info_hash(self,hash):
    #     self._vote_info_hash=hash
    
    
    # @commit_state_id.setter
    # def commit_state_id(self,state_id):
    #     self._commit_state_id=state_id


class LedgerCommitInfoSchema(Schema):
    commit_state_id = fields.Int()
    vote_info_hash = fields.Str()

    @post_load
    def to_object(self, data, **kwargs):
        data["vote_info_hash"] = bytes(data["vote_info_hash"], "utf-8")
        return LedgerCommitInfo(**data)


# x=LedgerCommitInfo()
# x.commit_state_id=10
# x.vote_info_hash=11
# print(x.commit_state_id,x.vote_info_hash)