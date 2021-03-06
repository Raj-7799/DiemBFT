import Util
from BlockTree import QC



import os

class TimeoutInfo():
    def __init__(self, roundNo: int, high_qc: QC, sender: int, pvt_key, pbc_key):
        self.roundNo = roundNo
        self.high_qc = high_qc
        self.sender = sender #// Added automatically when constructed
        #// Signed automatically when constructed
        self.signature = Util.sign_object_dup(self.form_signature_object(), pvt_key)

    def verify_self_signature(self, pbc_key):
        return Util.check_authenticity_dup(self.form_signature_object(), self.signature, pbc_key)
        
    def form_signature_object(self):
        return [self.roundNo, self.high_qc.vote_info.roundNo]

