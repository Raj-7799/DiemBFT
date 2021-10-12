from Quorum import QC
import Util

class TimeoutInfo():
    def __init__(self, round: int, high_qc: QC, sender: int, pvt_key, pbc_key):
        self.round = round
        self.high_qc = high_qc
        self.sender = sender
        self.signature = Util.sign_object(self.form_signature_object(), pvt_key, pbc_key)
    
    def verify_self_signature(self):
        return Util.check_authenticity(self.form_signature_object(), self.signature)

    def form_signature_object(self):
        return [self.round, self.sender]
