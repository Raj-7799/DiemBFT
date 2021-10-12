class TC:
#Since TC is used by Pacemaker module only, Its contruction requires all datafields to be declared
    def __init__(self, round: int):
        self.round = round
        self.tmo_high_qc_rounds = []
        self.tmo_signatures = []