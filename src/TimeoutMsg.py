from TimeoutInfo import TimeoutInfo
from TC import TC
from Quorum import QC

class TimeoutMsg():
    def __init__(self, tmo_info: TimeoutInfo, last_round_tc: TC, high_commit_qc: QC):
        self.tmo_info = tmo_info
        self.last_round_tc = last_round_tc
        self.high_commit_qc = high_commit_qc
