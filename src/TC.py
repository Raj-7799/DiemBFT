

import os
from diembft_logger import get_logger


class TC:
#Since TC is used by Pacemaker module only, Its contruction requires all datafields to be declared
    def __init__(self, roundNo: int, tmo_high_qc_rounds: list, tmo_signatures: list):
        self.roundNo = roundNo
        self.tmo_high_qc_rounds = tmo_high_qc_rounds
        self.tmo_signatures = tmo_signatures