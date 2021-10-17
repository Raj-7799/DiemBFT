import BlockTree as bt
import TimeoutInfo as Timeoutinfo
import Ledger as Ledger
import BlockTree as Blocktree
import random
from Safety import Safety
import Util
import os
from diembft_logger import get_logger

diem_logger = get_logger(os.path.basename(__file__))



class SafetyByz(Safety):

    def __init__(self, blocktree: bt.BlockTree, public_keys, sender,processByzantineSeed,degreeOfByzantine):
        Safety.__init__(self,blocktree,public_keys,sender)
        self.blocktree = blocktree
        self.ledger = self.blocktree._ledger
        self.private_key = self.blocktree.pvt_key
        self.public_keys = public_keys
        
        self.highest_vote_round = -1
        self.highest_qc_round = -1
        self.sender = sender
        self.pvt_key = self.private_key
        self.pbc_key = self.blocktree.pbc_key
        
        self.processByzantineSeed = processByzantineSeed
        self.degreeOfByzantine=degreeOfByzantine


    def make_vote(self, b, last_tc):
        qc_round = b.qc.vote_info.roundNo
        value =  Util.get_random(self.processByzantineSeed,self.degreeOfByzantine)
        
        print("Safety Byzantine replicaId {} for value generated {} for degree byzantine {} ".format(self.sender,value,self.degreeOfByzantine))
        if self._validate_signatures(b, last_tc) and self._safe_to_vote(b.roundNo, qc_round, last_tc) and (self.degreeOfByzantine==1 or value % (self.degreeOfByzantine//2)) == 0:
            self._update_highest_qc_round(qc_round)
            self._increase_highest_vote_round(b.roundNo)

            vote_info = bt.VoteInfo(id=b.id, roundNo=b.roundNo, parent_id=b.qc.vote_info.id, parent_round=b.qc.vote_info.roundNo,exec_state_id=self.ledger.pending_state(b.id))
            ledger_commit_info = bt.LedgerCommitInfo(self._commit_state_id_candidate(b.roundNo, b.qc), vote_info)

            return bt.VoteMsg(vote_info, ledger_commit_info, self.blocktree.high_commit_qc,self.sender,self.pvt_key,self.pbc_key)
        
        return None
