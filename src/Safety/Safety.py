from blockchain import LedgerCommitInfo
from vote import VoteInfo
from vote import VoteMsg

class Safety():

    def __init__(self, ledger, blocktree):
        self._ledger = ledger
        self._blocktree = blocktree
        self._private_key = None
        self._public_keys = None
        self._highest_vote_round = None
        self._highest_qc_round = None

    def increase_highest_vote_round(self, round):
        self._highest_vote_round = max(round, self._highest_vote_round)

    def update_highest_qc_round(self, qc_round):
        self._highest_qc_round = max(qc_round, self._highest_qc_round)

    def consecutive(self, block_round, round):
        return (round + 1) == block_round

    def safe_to_extend(self, block_round, qc_round, tc):
        return self.consecutive(block_round, tc.round) and (qc_round >= max(tc.tmo_high_qc_rounds))

    def safe_to_vote(self, block_round, qc_round, tc):
        if (block_round <= max(self._highest_vote_round, qc_round)):
            return False
        return self.consecutive(block_round, qc_round) or self.safe_to_extend(block_round, qc_round, tc)

    def safe_to_timeout(self, round, qc_round, tc):
        if (qc_round < self._highest_qc_round) or (round <= max((self._highest_vote_round - 1), qc_round)):
            return False
        return self.consecutive(round, qc_round) or self.consecutive(round, tc.round)

    def commit_state_id_candidate(self, block_round, qc):
        if self.consecutive(block_round, qc.vote_info.round):
            return self._ledger.pending_state(qc.id)
        else:
            return None
    'Safety: Private'

    def _valid_signatures(self, b, last_tc):
        return True

    def _hash(self, vote_info):
        return "hash of " + vote_info

    def make_vote(self, b, last_tc):
        qc_round = b.qc.vote_info.round
        if self._valid_signatures(b, last_tc) and self.safe_to_vote(b.round, qc_round, last_tc):
            self.update_highest_qc_round(qc_round)
            self.increase_highest_vote_round(b.round)
            vote_info = VoteInfo()
            vote_info.id = b.id
            vote_info.round = b.round
            vote_info.parent_id = b.qc.vote_info.id
            vote_info.parent_round = qc_round
            vote_info.exec_state_id = self._ledger.pending_state(b.id)
            ledger_commit_info = LedgerCommitInfo()
            ledger_commit_info.commit_state_id = self.commit_state_id_candidate(b.round, b.qc)
            ledger_commit_info.vote_info_hash = self._hash(b.round, b.qc)
            return VoteMsg(vote_info, ledger_commit_info, self._blocktree.high_commit_qc)
