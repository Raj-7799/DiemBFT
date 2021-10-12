from blockchain import LedgerCommitInfo as LedgerCommitInfo
from vote import VoteInfo as VI
from vote import VoteMsg as VoteMsg
from certificates.Timeout import TimeoutInfo as Timeoutinfo


class Safety():

    def __init__(self, ledger, blocktree):
        self._ledger = ledger
        self._blocktree = blocktree
        self._private_key = None
        self._public_keys = None
        self._highest_vote_round = None
        self._highest_qc_round = None

    def _increase_highest_vote_round(self, round):
        self._highest_vote_round = max(round, self._highest_vote_round)

    def _update_highest_qc_round(self, qc_round):
        self._highest_qc_round = max(qc_round, self._highest_qc_round)

    def _consecutive(self, block_round, round):
        return (round + 1) == block_round

    def _safe_to_extend(self, block_round, qc_round, tc):
        return self._consecutive(block_round, tc.round) and (qc_round >= max(tc.tmo_high_qc_rounds))

    def _safe_to_vote(self, block_round, qc_round, tc):
        if (block_round <= max(self._highest_vote_round, qc_round)):
            return False
        return self._consecutive(block_round, qc_round) or self._safe_to_extend(block_round, qc_round, tc)

    def _safe_to_timeout(self, round, qc_round, tc):
        if (qc_round < self._highest_qc_round) or (round <= max((self._highest_vote_round - 1), qc_round)):
            return False
        return self._consecutive(round, qc_round) or self._consecutive(round, tc.round)

    def _commit_state_id_candidate(self, block_round, qc):
        if self._consecutive(block_round, qc.vote_info.round):
            return self._ledger.pending_state(qc.id)
        else:
            return None
    
    '''Safety: Private'''
    #validate function currently always returns true
    def _validate_signatures(self, b, last_tc):
        #TODO
        return True

    def _hash(self, vote_info):
        #yet to be implemented
        return "hash of vote_info"

    def make_vote(self, b, last_tc):
        qc_round = b.qc.vote_info.round
        if self._validate_signatures(b, last_tc) and self._safe_to_vote(b.round, qc_round, last_tc):
            self._update_highest_qc_round(qc_round)
            self._increase_highest_vote_round(b.round)
            vote_info = VI.VoteInfo()
            vote_info.id = b.id
            vote_info.round = b.round
            vote_info.parent_id = b.qc.vote_info.id
            vote_info.parent_round = qc_round
            vote_info.exec_state_id = self._ledger.pending_state(b.id)
            ledger_commit_info = LedgerCommitInfo.LedgerCommitInfo()
            ledger_commit_info.commit_state_id = self._commit_state_id_candidate(b.round, b.qc)
            ledger_commit_info.vote_info_hash = self._hash(vote_info)
            return VoteMsg.VoteMsg(vote_info, ledger_commit_info, self._blocktree.high_commit_qc)

    def make_timeout(self, round, high_qc, last_tc):
        qc_round = high_qc.vote_info.round
        if self._validate_signatures(high_qc, last_tc) and self._safe_to_timeout(round, qc_round, last_tc):
            self._increase_highest_vote_round(round)
            timeoutinfo = Timeoutinfo.TimeoutInfo()
            timeoutinfo.round = round
            timeoutinfo.high_qc = high_qc
            return timeoutinfo
        return None

