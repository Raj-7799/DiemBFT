from TC import TC
from BlockTree import QC, Block
import Util
import sys

class ProposalMsg:
    def __init__(self, block: Block, last_round_tc: TC, high_commit_qc: QC, pvt_key, pbc_key):
        self.block = block
        self.last_round_tc = last_round_tc
        self.high_commit_qc = high_commit_qc
        self.signature = Util.sign_object(self.block.id, pvt_key, pbc_key)


