class TimeoutInfo():
    def __init__(self, round, high_qc):
        self._round = round
        self._high_qc = high_qc
        self._sender = None#Implement sender<-u
        self._signature = None#Implement signature<-signU(round, high_qc.round)


    @property
    def round(self):
        return self._round


    @property
    def high_qc(self):
        return self._high_qc


    @property
    def sender(self):
        return self._sender


    @property
    def signature(self):
        return self._signature