from TC import TC
from BlockTree import QC, Block
import Util
import sys


import os

class ProposalMsg:
    def __init__(self, block: Block, last_round_tc: TC, high_commit_qc: QC, pvt_key, pbc_key):
        self.block = block
        self.last_round_tc = last_round_tc #  // TC for block.round −1 if block.qc.vote info.round 6= block.round −1, else ⊥
        self.high_commit_qc = high_commit_qc # QC to synchronize on committed blocks
        
        self.signature = Util.sign_object_dup(self.block.id, pvt_key)
    
    def __str__(self):
        return "{ Block - {} Last_round_tc - {} High_commit_qc - {} }".format(self.block, self.last_round_tc, self.high_commit_qc)


