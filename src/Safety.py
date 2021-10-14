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
        
        self.highest_vote_round = 0
        self.highest_qc_round = 0
        self.sender = sender
        self.pvt_key = self.private_key
        self.pbc_key = self.blocktree.pbc_key

    def _increase_highest_vote_round(self, roundNo):
        diem_logger.info("[Safety][replicaID {}] START _increase_highest_vote_round for roundNo {}".format(self.sender, roundNo))
        self.highest_vote_round = max(roundNo, self.highest_vote_round)
        diem_logger.info("[Safety][replicaID {}] END _increase_highest_vote_round for roundNO {}".format(self.sender, roundNo))

    def _update_highest_qc_round(self, qc_round):
        diem_logger.info("[Safety][replicaID {}] START _update_highest_qc_round for qc_round {} ".format(self.sender, qc_round))
        self.highest_qc_round = max(qc_round, self.highest_qc_round)
        diem_logger.info("[Safety][replicaID {}] END _update_highest_qc_round for qc_round {} ".format(self.sender, qc_round))

    def _consecutive(self, block_round, roundNo):
        diem_logger.info("[Safety][replicaID {}] START _consecutive with block_round {} and roundNo {}".format(self.sender, block_round, roundNo))
        return (roundNo + 1) == block_round

    def _safe_to_extend(self, block_round, qc_round, tc):
        #max_tmo_high_qc = max()
        diem_logger.info("[Safety][replicaID {}] START _safe_to_extend with block_round {} and qc_round {}".format(self.sender, block_round, qc_round))
        return self._consecutive(block_round, tc.roundNo) and (qc_round >= max(tc.tmo_high_qc_rounds))

    def _safe_to_vote(self, block_round, qc_round, tc):
        diem_logger.info("[Safety][replicaID {}] START _safe_to_vote with block_round {} and qc_round {}".format(self.sender, block_round, qc_round))
        if (block_round <= max(self.highest_vote_round, qc_round)):
            return False
        diem_logger.info("[Safety][replicaID {}] END _safe_to_vote with block_round {} and qc_round {}".format(self.sender, block_round, qc_round))
        return self._consecutive(block_round, qc_round) or self._safe_to_extend(block_round, qc_round, tc)

    def _safe_to_timeout(self, roundNo, qc_round, tc):
        diem_logger.info("[Safety][replicaID {}] START _safe_to_timeout with roundNo {} and qc_round {}".format(self.sender, roundNo, qc_round))
        if (qc_round < self.highest_qc_round) or (roundNo <= max((self.highest_vote_round - 1), qc_round)):
            return False
        diem_logger.info("[Safety][replicaID {}] END _safe_to_timeout with roundNo {} and qc_round {}".format(self.sender, roundNo, qc_round))
        return self._consecutive(roundNo, qc_round) or self._consecutive(roundNo, tc.roundNo)

    def _commit_state_id_candidate(self, block_round, qc):
        diem_logger.info("[Safety][replicaID {}] START _commit_state_id_candidate with block_round {} and qc.vote_info.roundNo {}".format(self.sender, block_round, qc.vote_info.roundNo))
        if self._consecutive(block_round, qc.vote_info.roundNo):
            #In Paper-> Ledger.pending state(qc.id)
            # Qc has not attribute as id
            diem_logger.info("[Safety][replicaID {}] END _commit_state_id_candidate with block_round {} and qc.vote_info.roundNo {}".format(self.sender, block_round, qc.vote_info.roundNo))
            return self.ledger.pending_state(qc.vote_info.parent_id)
        else:
            return None
    
    '''Safety: Private'''
    #validate function currently always returns true
    def _validate_signatures(self, b, last_tc):
        #TODO
        return True

    def make_vote(self, b, last_tc):
        diem_logger.info("[Safety][replicaID {}] START make_vote with b.qc.vote_info.roundNo {}".format(self.sender, b.qc.vote_info.roundNo))
        qc_round = b.qc.vote_info.roundNo
        if self._validate_signatures(b, last_tc) and self._safe_to_vote(b.roundNo, qc_round, last_tc):
            self._update_highest_qc_round(qc_round)
            self._increase_highest_vote_round(b.roundNo)

            vote_info = bt.VoteInfo(id=b.id, roundNo=b.roundNo, parent_id=b.qc.vote_info.id, parent_round=b.qc.vote_info.roundNo,exec_state_id=self.ledger.pending_state(b.id))
            ledger_commit_info = bt.LedgerCommitInfo(self._commit_state_id_candidate(b.roundNo, b.qc), vote_info)
            diem_logger.info("[Safety][replicaID {}] END make_vote with b.qc.vote_info.roundNo {}".format(self.sender, b.qc.vote_info.roundNo))
            return bt.VoteMsg(vote_info, ledger_commit_info, self.blocktree.high_commit_qc,self.sender,self.pvt_key,self.pbc_key)
        diem_logger.info("[Safety][replicaID {}] END make_vote with b.qc.vote_info.roundNo {} without makeing Vote".format(self.sender, b.qc.vote_info.roundNo))
        return None

    def make_timeout(self, roundNo, high_qc, last_tc):
        diem_logger.info("[Safety][replicaID {}] START make_timeout with roundNo {} and high_qc.vote_info.roundNo {}".format(self.sender, roundNo, high_qc.vote_info.roundNo))
        qc_round = high_qc.vote_info.roundNo
        if self._validate_signatures(high_qc, last_tc) and self._safe_to_timeout(roundNo, qc_round, last_tc):
            self._increase_highest_vote_round(roundNo)
            timeoutinfo = Timeoutinfo.TimeoutInfo(roundNo, high_qc, self.sender, self.pvt_key, self.pbc_key)
            diem_logger.info("[Safety][replicaID {}] END make_timeout with roundNo {} and high_qc.vote_info.roundNo {}".format(self.sender, roundNo, high_qc.vote_info.roundNo))
            return timeoutinfo
        diem_logger.info("[Safety][replicaID {}] END make_timeout with roundNo {} and high_qc.vote_info.roundNo {} without returning timeout".format(self.sender, roundNo, high_qc.vote_info.roundNo))
        return None

