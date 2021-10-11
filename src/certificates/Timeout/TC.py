class TC():
#Since TC is used by Pacemaker module only, Its contruction requires all datafields to be declared
    def __init__(self, round, tmo_high_qc_rounds, tmo_signatures):
        self._round = round
        self._tmo_high_qc_rounds = tmo_high_qc_rounds#used in Safety:safe_to_extend
        self._tmo_signatures = tmo_signatures


    @property
    def round(self):
        return self._round

    @round.setter
    def round(self, round):
        self._round = round

    @property
    def tmo_high_qc_rounds(self):
        return self._tmo_high_qc_rounds

    @tmo_high_qc_rounds.setter
    def tmo_high_qc_rounds(self, tmo_high_qc_rounds):
        self._tmo_high_qc_rounds = tmo_high_qc_rounds

    @property
    def tmo_signatures(self):
        return self._tmo_signatures

    @tmo_signatures.setter
    def tmo_signatures(self, tmo_signatures):
        self._tmo_signatures = tmo_signatures
