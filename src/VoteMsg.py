from nacl import utils
from Keys import Keys as keys
from LedgerCommitInfo import LedgerCommitInfo as ledgerCommitInfo
from VoteInfo import VoteInfo as voteInfo
from Quorum import QC 
import Util

class VoteMsg:

    def __init__(self, vote_info: voteInfo, ledger_commit_info: ledgerCommitInfo, high_commit_qc: QC, sender: int, pvt_key, pbc_key):
        self.vote_info = vote_info
        self.ledger_commit_info = ledger_commit_info
        self.high_commit_qc = high_commit_qc
        self.sender = sender
        self.signature = Util.sign_object(self.form_signature_object(), pvt_key, pbc_key)#key.sign_message(self._ledger_commit_info) 
        
    def verify_self_signature(self):
        return Util.check_authenticity(self.form_signature_object(), self.signature)

    def form_signature_object(self):
        return [self.ledger_commit_info]

    