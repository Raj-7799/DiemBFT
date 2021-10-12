import Util

class LedgerCommitInfo:
    def __init__(self, commit_state_id, vote_info_hash):
        self.commit_state_id = commit_state_id
        self.vote_info_hash = Utils.hash(vote_info_hash)