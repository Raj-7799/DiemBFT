# -*- generated by 1.0.14 -*-
import da
PatternExpr_221 = da.pat.TuplePattern([da.pat.ConstantPattern('Yo bro')])
PatternExpr_241 = da.pat.TuplePattern([da.pat.ConstantPattern('Yo boiii')])
PatternExpr_246 = da.pat.FreePattern('source')
_config_object = {}
import sys
from client import client

class Replica(da.DistProcess):

    def __init__(self, procimpl, props):
        super().__init__(procimpl, props)
        self._ReplicaSentEvent_0 = []
        self._events.extend([da.pat.EventPattern(da.pat.SentEvent, '_ReplicaSentEvent_0', PatternExpr_221, sources=None, destinations=None, timestamps=None, record_history=True, handlers=[]), da.pat.EventPattern(da.pat.ReceivedEvent, '_ReplicaReceivedEvent_1', PatternExpr_241, sources=[PatternExpr_246], destinations=None, timestamps=None, record_history=None, handlers=[self._Replica_handler_240])])

    def setup(self, pID, other_replicas, faulty_replica_count, replica_count, delta, **rest_255):
        super().setup(pID=pID, other_replicas=other_replicas, faulty_replica_count=faulty_replica_count, replica_count=replica_count, delta=delta, **rest_255)
        self._state.pID = pID
        self._state.other_replicas = other_replicas
        self._state.faulty_replica_count = faulty_replica_count
        self._state.replica_count = replica_count
        self._state.delta = delta
        self._state.pID = self._state.pID
        self._state.replicas = self._state.other_replicas
        self._state.fCount = self._state.faulty_replica_count
        self._state.rCount = self._state.replica_count
        self._state.tDelta = self._state.delta

    def run(self):
        self.output('Yo Starting replica with pID', self._state.pID)
        super()._label('_st_label_218', block=False)

        def ExistentialOpExpr_219():
            for (_, _, (_ConstantPattern234_,)) in self._ReplicaSentEvent_0:
                if (_ConstantPattern234_ == 'Yo bro'):
                    if True:
                        return True
            return False
        _st_label_218 = 0
        while (_st_label_218 == 0):
            _st_label_218 += 1
            if ExistentialOpExpr_219():
                _st_label_218 += 1
            else:
                super()._label('_st_label_218', block=True)
                _st_label_218 -= 1

    def _Replica_handler_240(self, source):
        self.output('Replying back')
        self.send(('Yo bro',), to=source)
    _Replica_handler_240._labels = None
    _Replica_handler_240._notlabels = None
