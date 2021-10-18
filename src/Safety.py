import BlockTree as bt
import TimeoutInfo as Timeoutinfo
import Ledger as Ledger
import BlockTree as Blocktree



import os



class Safety():

    def __init__(self, blocktree: bt.BlockTree, public_keys, sender,OutputLogger):
        self.blocktree = blocktree
        self.ledger = self.blocktree._ledger
        self.private_key = self.blocktree.pvt_key
        self.public_keys = public_keys #// Public keys of all validators
        
        self.highest_vote_round = -1  #// initially 0 , we have set it -1 in accordance with the genesis block round 
        self.highest_qc_round = -1
        self.sender = sender
        self.pvt_key = self.private_key # // Own private key
        self.pbc_key = self.blocktree.pbc_key
        
        self.OutputLogger=OutputLogger
        self.OutputLogger("__init__")
    def _increase_highest_vote_round(self, roundNo):
        # commit not to vote in rounds lower than round
        self.highest_vote_round = max(roundNo, self.highest_vote_round)

    def _update_highest_qc_round(self, qc_round):
        self.highest_qc_round = max(qc_round, self.highest_qc_round)

    def _consecutive(self, block_round, roundNo):
        return (roundNo + 1) == block_round

    def _safe_to_extend(self, block_round, qc_round, tc):
        if tc is None:
            return True
        return self._consecutive(block_round, tc.roundNo) and (qc_round >= max(tc.tmo_high_qc_rounds))

    def _safe_to_vote(self, block_round, qc_round, tc):

        if (block_round <= max(self.highest_vote_round, qc_round)):
            # // 1. must vote in monotonically increasing rounds
            # // 2. must extend a smaller round
            self.OutputLogger("[_safe_to_vote] Block round {} is less than qc_round {} or high vote round {}".format(block_round, qc_round, self.highest_vote_round))
            return False
            # // Extending qc from previous round or safe to extend due to tc
        return self._consecutive(block_round, qc_round) or self._safe_to_extend(block_round, qc_round, tc)

    def _safe_to_timeout(self, roundNo, qc_round, tc):
        # // respect highest qc round and don’t timeout in a past round
        if (qc_round < self.highest_qc_round) or (roundNo <= max((self.highest_vote_round - 1), qc_round)):
            return False
        
        consecutive_qc = self._consecutive(roundNo, qc_round)
        consecutive_tc = self._consecutive(roundNo, tc.roundNo) if tc is not None else True
        # // qc or tc must allow entering the round to timeout
        return consecutive_qc or consecutive_tc

    def _commit_state_id_candidate(self, block_round, qc):
        #// find the committed id in case a qc is formed in the vote round
        if self._consecutive(block_round, qc.vote_info.roundNo):
            #In Paper-> Ledger.pending state(qc.id)
            # Qc has not attribute as id
            pending_state = self.ledger.pending_state(qc.vote_info.id)
            self.OutputLogger("[_commit_state_id_candidate] Pending state returned for block_round {}".format(pending_state))
            return pending_state
        else:
            return None
    
    '''Safety: Private'''
    def _validate_signatures(self, qc, last_tc):
        #TODO
        if ((last_tc is None) or last_tc.verify_self_signature()) and (qc.verify_self_signature_qc()):
            self.OutputLogger("Safety validation successsful")
            return True
        else:
            self.OutputLogger("Safety validation failed")
            return False

    def make_vote(self, b, last_tc):
        self.OutputLogger("[make_vote] Entry")
        qc_round = b.qc.vote_info.roundNo
        if self._validate_signatures(b.qc, last_tc) and self._safe_to_vote(b.roundNo, qc_round, last_tc):
            self._update_highest_qc_round(qc_round) # // Protect qc round
            self._increase_highest_vote_round(b.roundNo) # // Don’t vote again in this (or lower) round
            # // VoteInfo carries the potential QC info with ids and rounds of the parent QC
            vote_info = bt.VoteInfo(id=b.id, roundNo=b.roundNo, parent_id=b.qc.vote_info.id, parent_round=b.qc.vote_info.roundNo,exec_state_id=self.ledger.pending_state(b.id))
            ledger_commit_info = bt.LedgerCommitInfo(self._commit_state_id_candidate(b.roundNo, b.qc), vote_info)
            self.OutputLogger("[make_vote] Exit returning vote msg")
            return bt.VoteMsg(vote_info, ledger_commit_info, self.blocktree.high_commit_qc,self.sender,self.pvt_key,self.pbc_key)
        self.OutputLogger("[make_vote] Exit returning None")
        return None

    def make_timeout(self, roundNo, high_qc, last_tc):
        self.OutputLogger("[make_timeout] Entry")

        qc_round = high_qc.vote_info.roundNo

        if self._validate_signatures(high_qc, last_tc) and self._safe_to_timeout(roundNo, qc_round, last_tc):
            self._increase_highest_vote_round(roundNo) # // Stop voting for round
            timeoutinfo = Timeoutinfo.TimeoutInfo(roundNo, high_qc, self.sender, self.pvt_key, self.pbc_key)
            self.OutputLogger("[make_timeout] Exit returning timeoutinfo")

            return timeoutinfo
        self.OutputLogger("[make_timeout] Exit returning None")
        return None

