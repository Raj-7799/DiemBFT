

import os
from diembft_logger import get_logger
import Util
import pickle

diem_logger = get_logger(os.path.basename(__file__))

class TC:
#Since TC is used by Pacemaker module only, Its contruction requires all datafields to be declared
    def __init__(self, roundNo: int, tmo_high_qc_rounds: list, tmo_signatures: list, pvt_key, pbc_key):
        self.roundNo = roundNo
        self.tmo_high_qc_rounds = tmo_high_qc_rounds
        self.tmo_signatures = tmo_signatures
        #self.hash = Util.hash(pickle.dumps(self.get_block_identity_object()))
        self.pvt_key = pvt_key
        self.pbc_key = pbc_key
        self.signature = Util.sign_object_dup(self.get_block_identity_object(), pvt_key)

        if self.verify_self_signature():
            print("TC Validtion successfull")
        else:
            print("TC Validtion failed")

    def get_block_identity_object(self):
        return [self.roundNo, self.tmo_high_qc_rounds, self.tmo_signatures]
    
    def verify_self_signature(self):
        #hash = Util.hash(pickle.dumps(self.get_block_identity_object()))
        return Util.check_authenticity_dup(self.get_block_identity_object(), self.signature, self.pbc_key)