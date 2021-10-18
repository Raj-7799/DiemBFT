import Util
from BlockTree import QC



import os
from diembft_logger import get_logger

diem_logger = get_logger(os.path.basename(__file__))


class TimeoutInfo():
    def __init__(self, roundNo: int, high_qc: QC, sender: int, pvt_key, pbc_key):
        self.roundNo = roundNo
        self.high_qc = high_qc
        self.sender = sender
        self.signature = Util.sign_object_dup(self.form_signature_object(), pvt_key)
    


    def verify_self_signature(self, pbc_key):
        return Util.check_authenticity_dup(self.form_signature_object(), self.signature, pbc_key)
    def form_signature_object(self):
        return [self.roundNo, self.high_qc.vote_info.roundNo]

