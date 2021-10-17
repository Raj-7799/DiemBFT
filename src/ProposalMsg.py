from TC import TC
from BlockTree import QC, Block
import Util
import sys


import os
from diembft_logger import get_logger

diem_logger = get_logger(os.path.basename(__file__))

class ProposalMsg:
    def __init__(self, block: Block, last_round_tc: TC, high_commit_qc: QC, pvt_key, pbc_key):
        self.block = block
        self.last_round_tc = last_round_tc
        self.high_commit_qc = high_commit_qc
        self.signature = Util.sign_object(self.block.id, pvt_key, pbc_key)
    
    def __str__(self):
        return "{ Block - {} \n Last_round_tc - {} \n High_commit_qc - {} }".format(self.block, self.last_round_tc, self.high_commit_qc)


