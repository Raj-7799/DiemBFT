class TimeoutMsg():
    def __init__(self, tmo_info , last_round_tc, high_commit_qc):
        self._tmo_info = tmo_info
        self._last_round_tc = last_round_tc
        self._high_commit_qc = high_commit_qc


    @property
    def tmo_info(self):
        return self._tmo_info

    @property
    def last_round_tc(self):
        return self._last_round_tc

    @property
    def high_commit_qc(self):
        return self._high_commit_qc