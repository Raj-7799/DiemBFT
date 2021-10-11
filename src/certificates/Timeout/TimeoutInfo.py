class TimeoutInfo():
    def __init__(self, round, high_qc):
        self._round = round
        self._high_qc = high_qc
        self._sender = None#Implement sender<-u
        self._signature = None#Implement signature<-signU(round, high_qc.round)


    @property
    def round(self):
        return self._round

    @round.setter
    def round(self, round):
        self._round = round

    @property
    def high_qc(self):
        return self._high_qc

    @high_qc.setter
    def high_qc(self, high_qc):
        self._high_qc = high_qc

    @property
    def sender(self):
        return self._sender

    @sender.setter
    def sender(self, sender):
        self._sender = sender

    @property
    def signature(self):
        return self._signature
    
    @signature.setter
    def signature(self, signature):
        self._signature = signature