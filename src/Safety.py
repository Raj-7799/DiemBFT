import BlockTree as bt
import TimeoutInfo as Timeoutinfo
import Ledger as Ledger
import BlockTree as Blocktree



import os
from diembft_logger import get_logger

diem_logger = get_logger(os.path.basename(__file__))



class Safety():

    def __init__(self, blocktree: bt.BlockTree, public_keys, sender):
        self.blocktree = blocktree
        self.ledger = self.blocktree._ledger
        self.private_key = self.blocktree.pvt_key
        self.public_keys = public_keys
        
        self.highest_vote_round = -1
        self.highest_qc_round = -1
        self.sender = sender
        self.pvt_key = self.private_key
        self.pbc_key = self.blocktree.pbc_key

    def _increase_highest_vote_round(self, roundNo):
        # print("[replicaID {}] Block round {} is less than qc_round {} or high vote round {}".format(self.sender, block_round, qc_round, self.highest_vote_round))
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
            print("[replicaID {}] Block round {} is less than qc_round {} or high vote round {}".format(self.sender, block_round, qc_round, self.highest_vote_round))
            return False
        return self._consecutive(block_round, qc_round) or self._safe_to_extend(block_round, qc_round, tc)

    def _safe_to_timeout(self, roundNo, qc_round, tc):
        if (qc_round < self.highest_qc_round) or (roundNo <= max((self.highest_vote_round - 1), qc_round)):
            return False
        
        consecutive_qc = self._consecutive(roundNo, qc_round)
        consecutive_tc = self._consecutive(roundNo, tc.roundNo) if tc is not None else True
        return consecutive_qc or consecutive_tc

    def _commit_state_id_candidate(self, block_round, qc):
        if self._consecutive(block_round, qc.vote_info.roundNo):
            #In Paper-> Ledger.pending state(qc.id)
            # Qc has not attribute as id
            pending_state = self.ledger.pending_state(qc.vote_info.id)
            print("Pending state returned for block_round {}".format(pending_state))
            return pending_state
        else:
            return None
    
    '''Safety: Private'''
    #validate function currently always returns true
    def _validate_signatures(self, qc, last_tc):
        #TODO
        #print("Safety validation" + str(type(qc)))
        if ((last_tc is None) or last_tc.verify_self_signature()) and (qc.verify_self_signature_qc()):
            print("Safety validation successsful")
            return True
        else:
            print("Safety validation failed")
            return False

    def make_vote(self, b, last_tc):
        qc_round = b.qc.vote_info.roundNo
        if self._validate_signatures(b.qc, last_tc) and self._safe_to_vote(b.roundNo, qc_round, last_tc):
            self._update_highest_qc_round(qc_round)
            self._increase_highest_vote_round(b.roundNo)

            vote_info = bt.VoteInfo(id=b.id, roundNo=b.roundNo, parent_id=b.qc.vote_info.id, parent_round=b.qc.vote_info.roundNo,exec_state_id=self.ledger.pending_state(b.id))
            ledger_commit_info = bt.LedgerCommitInfo(self._commit_state_id_candidate(b.roundNo, b.qc), vote_info)

            return bt.VoteMsg(vote_info, ledger_commit_info, self.blocktree.high_commit_qc,self.sender,self.pvt_key,self.pbc_key)
        
        return None

    def make_timeout(self, roundNo, high_qc, last_tc):
        print("Inside make timeout")

        qc_round = high_qc.vote_info.roundNo
        print("Validate signatures", self._validate_signatures(high_qc, last_tc))
        print("Safe to timeout", self._safe_to_timeout(roundNo, qc_round, last_tc))
        print("High QC is ", high_qc)

        if self._validate_signatures(high_qc, last_tc) and self._safe_to_timeout(roundNo, qc_round, last_tc):
            self._increase_highest_vote_round(roundNo)
            timeoutinfo = Timeoutinfo.TimeoutInfo(roundNo, high_qc, self.sender, self.pvt_key, self.pbc_key)
            return timeoutinfo
        
        return None

