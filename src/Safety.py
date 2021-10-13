import BlockTree as bt
import TimeoutInfo as Timeoutinfo


class Safety():

    def __init__(self, ledger, blocktree, private_key, public_keys, highest_vote_round, highest_qc_round, sender, pvt_key, pbc_key):
        self.ledger = ledger
        self.blocktree = blocktree
        self.private_key = private_key
        self.public_keys = public_keys
        self.highest_vote_round = highest_vote_round
        self.highest_qc_round = highest_qc_round
        self.sender = sender
        self.pvt_key = pvt_key
        self.pbc_key = pbc_key

    def _increase_highest_vote_round(self, roundNo):
        self.highest_vote_round = max(roundNo, self.highest_vote_round)

    def _update_highest_qc_round(self, qc_round):
        self.highest_qc_round = max(qc_round, self.highest_qc_round)

    def _consecutive(self, block_round, roundNo):
        return (roundNo + 1) == block_round

    def _safe_to_extend(self, block_round, qc_round, tc):
        return self._consecutive(block_round, tc.round) and (qc_round >= max(tc.tmo_high_qc_rounds))

    def _safe_to_vote(self, block_round, qc_round, tc):
        if (block_round <= max(self.highest_vote_round, qc_round)):
            return False
        return self._consecutive(block_round, qc_round) or self._safe_to_extend(block_round, qc_round, tc)

    def _safe_to_timeout(self, roundNo, qc_round, tc):
        if (qc_round < self.highest_qc_round) or (roundNo <= max((self.highest_vote_round - 1), qc_round)):
            return False
        return self._consecutive(roundNo, qc_round) or self._consecutive(roundNo, tc.round)

    def _commit_state_id_candidate(self, block_round, qc):
        if self._consecutive(block_round, qc.vote_info.round):
            return self.ledger.pending_state(qc.id)
        else:
            return None
    
    '''Safety: Private'''
    #validate function currently always returns true
    def _validate_signatures(self, b, last_tc):
        #TODO
        return True

    def make_vote(self, b, last_tc):
        qc_round = b.qc.vote_info.roundNo
        if self._validate_signatures(b, last_tc) and self._safe_to_vote(b.roundNo, qc_round, last_tc):
            self._update_highest_qc_round(qc_round)
            self._increase_highest_vote_round(b.roundNo)
            vote_info = bt.VoteInfo(b.id, b.roundNo, b.qc.vote_info.id, self.ledger.pending_state(b.id))
            ledger_commit_info = bt.LedgerCommitInfo(self._commit_state_id_candidate(b.roundNo, b.qc), vote_info)

            return bt.VoteMsg(vote_info, ledger_commit_info, self.blocktree.high_commit_qc)
        
        return None

    def make_timeout(self, roundNo, high_qc, last_tc):
        qc_round = high_qc.vote_info.roundNo
        if self._validate_signatures(high_qc, last_tc) and self._safe_to_timeout(roundNo, qc_round, last_tc):
            self._increase_highest_vote_round(roundNo)
            timeoutinfo = Timeoutinfo.TimeoutInfo(roundNo, high_qc, self.sender, self.pvt_key, self.pbc_key)
            return timeoutinfo
        
        return None

