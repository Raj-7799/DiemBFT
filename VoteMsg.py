# VoteMsg
# vote_info; // A VoteInfo record
# ledger_commit_info; // Speculated ledger info
# high_commit_qc; // QC to synchronize on committed blocks
# sender ← u; // Added automatically when constructed
# signature ← sign u (ledger commit info); // Signed automatically when constructed

class VoteMsg:

    def __init__(self,u):
        self._vote_info=None
        self._ledger_commit_qc=None
        self._high_commit_qc=None
        self._sender=list()
        self._sender.append(u)
        self.signature=list()
        self.