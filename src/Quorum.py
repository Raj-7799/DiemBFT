from VoteInfo import VoteInfo
from LedgerCommitInfo import LedgerCommitInfo
import Keys as keys
import Util

class QC():
    def __init__(self,vote_info :VoteInfo, ledger_commit_info :LedgerCommitInfo, votes, author:int, pvt_key, pbc_key):
        self.vote_info          = vote_info
        self.ledger_commit_info = ledger_commit_info
        self.signatures         = votes
        self.author             = author
        self.signature          = Util.sign_object(self.signatures, pvt_key, pbc_key)
