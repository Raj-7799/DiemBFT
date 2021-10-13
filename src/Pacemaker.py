import TimeoutMsg as timeoutmsg
import TC as Tc
import threading
from collections import defaultdict


class Pacemaker:
    def __init__(self, safety, blocktree, delta, fCount, replica_broadcast):
        self.safety = safety
        self.blocktree = blocktree
        self.delta = delta
        self.fCount = fCount
        self.replica_broadcast = replica_broadcast
        self.current_round = 0
        self.last_round_tc = None
        self.pending_timeouts = defaultdict(set)  #dict of sets of pending timeouts for a round
        self.dict_of_timer = {} # dict of timer for a round


    def get_round_timer(self):
        # return 4 * float(int(self.delta)/1000) # Convert Millisecond to second
        return 4 * int(self.delta) // 1000

    def _on_timeout(self):
        #self.replica_broadcast(None)
        self.local_timeout_round()

    def _start_timer(self, roundNo):
        print("Starting new timer for round ", roundNo)
        self.dict_of_timer[roundNo] = threading.Timer(self.get_round_timer(), self._on_timeout)
        self.dict_of_timer[roundNo].start()
        print("Starting new timer for round ends ", roundNo)

    def _stop_timer(self, roundNo):
        if roundNo in self.dict_of_timer:
            self.dict_of_timer[roundNo].cancel()

    def start_timer(self, new_round):
        print("Starting timer for round ", new_round)
        self._stop_timer(self.current_round)
        self.current_round = new_round
        self._start_timer(self.current_round)

    def local_timeout_round(self):
        timeout_info = self.safety.make_timeout(self.current_round, self.blocktree.high_qc, self.last_round_tc)
        timeout_msg = timeoutmsg.TimeoutMsg(timeout_info, self.last_round_tc, self.blocktree.high_qc)
        self.replica_broadcast(timeout_msg)

    def _check_if_sender_pending(self, sender, tmo_info):
        for pending_tmo_info in self.pending_timeouts[tmo_info.roundNo]:
            if sender == pending_tmo_info.sender:
                return True
        return False

    def process_remote_timeout(self, tmo):
        print("Processing remote timeout")
        tmo_info = tmo.tmo_info
        if tmo_info.roundNo < self.current_round:
            return None
        if not self._check_if_sender_pending(tmo_info.sender, tmo_info):
            self.pending_timeouts[tmo_info.roundNo].add(tmo_info)
        if len(self.pending_timeouts[tmo_info.roundNo]) == self.fCount + 1:
            self._stop_timer(self.current_round)
            self.local_timeout_round()  #  Bracha timeout
        if len(self.pending_timeouts[tmo_info.roundNo]) == (2 * self.fCount) + 1:
            tmo_high_qc_rounds = []
            tmo_signatures = []
            for _tmo_info in list(self.pending_timeouts[tmo_info.roundNo]):
                tmo_high_qc_rounds.append(_tmo_info.high_qc.vote_info.roundNo)
                tmo_signatures.append(_tmo_info.signature)
            
            tc = Tc.TC(tmo_info.roundNo, tmo_high_qc_rounds, tmo_signatures)
            return tc
        return None

    def advance_round_tc(self, tc):
        if (tc is None) or (tc.roundNo < self.current_round):
            return False
        self.last_round_tc = tc
        self.start_timer(tc.roundNo + 1)
        return True

    def advance_round_qc(self, qc):
        if qc.vote_info.roundNo < self.current_round:
            return False
        self.last_round_tc = None
        self.start_timer(qc.vote_info.roundNo + 1)
        return True
