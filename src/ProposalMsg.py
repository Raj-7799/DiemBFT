class ProposalMsg ():
    def __init__(self, block, last_round_tc, high_commit_qc):
        self._block = block
        self._last_round_tc = last_round_tc
        self._high_commit_qc = high_commit_qc #Implement sender<-u
        self._signature = None #Implement signature<-signU(round, high_qc.round)

    @property
    def block(self):
        return self._block

    @block.setter
    def block(self, block):
        self._block = block

    @property
    def last_round_tc(self):
        return self._last_round_tc

    @last_round_tc.setter
    def last_round_tc(self, last_round_tc):
        self._last_round_tc = last_round_tc

    @property
    def high_commit_qc(self):
        return self._high_commit_qc

    @high_commit_qc.setter
    def high_commit_qc(self, high_commit_qc):
        self._high_commit_qc = high_commit_qc

    @property
    def signature(self):
        return self._signature

    @signature.setter
    def signature(self, signature):
        self._signature = signature
