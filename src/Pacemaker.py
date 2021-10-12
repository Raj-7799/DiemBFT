import TimeoutMsg as timeoutmsg
import TC as Tc
import threading


class Pacemaker:
    def __init__(self, safety, blocktree, delta, fCount, replica_broadcast):
        self._safety = safety
        self._blocktree = blocktree
        self._delta = delta
        self._fCount = fCount
        self._replica_broadcast = replica_broadcast
        self._current_round = 0
        self._last_round_tc = None
        self._pending_timeouts = {}  #dict of sets of pending timeouts for a round
        self._dict_of_timer = {} # dict of timer for a round


    def get_round_timer(self):
        return 4 * float(int(self._delta)/1000) # Convert Millisecond to second

    def _on_timeout(self):
        #self._replica_broadcast(None)
        self.local_timeout_round()

    def _start_timer(self, round):
        self._dict_of_timer[round] = threading.Timer(self.get_round_timer(), self._on_timeout())
        self._dict_of_timer[round].start()

    def _stop_timer(self, round):
        if round in self._dict_of_timer:
            self._dict_of_timer[round].cancel()

    def start_timer(self, new_round):
        self._stop_timer(self._current_round)
        self._current_round = new_round
        self._start_timer(round)

    def local_timeout_round(self):
        timeout_info = self._safety.make_timeout(self._current_round, self._blocktree.high_qc, self._last_round_tc)
        timeout_msg = timeoutmsg.TimeoutMsg()
        timeout_msg.tmo_info = timeout_info
        timeout_msg.high_commit_qc = self._blocktree.high_qc
        timeout_msg.last_round_tc = timeout_info
        self._replica_broadcast(timeout_msg)

    def _check_if_sender_pending(self, sender, tmo_info):
        for pending_tmo_info in self._pending_timeouts[tmo_info.round]:
            if sender == pending_tmo_info.sender:
                return True
        return False

    def process_remote_timeout(self, tmo):
        tmo_info = tmo.tmo_info
        if tmo_info.round < self._current_round:
            return None
        if not self._check_if_sender_pending(tmo_info.sender, tmo_info):
            self._pending_timeouts[tmo_info.round].append(tmo_info)
        if len(self._pending_timeouts[tmo_info.round]) == self._fCount + 1:
            self._stop_timer(self._current_round)
            self.local_timeout_round()  #  Bracha timeout
        if len(self._pending_timeouts[tmo_info.round]) == (2 * self._fCount) + 1:
            tmo_high_qc_rounds = []
            tmo_signatures = []
            for _tmo_info in self._pending_timeouts[tmo_info.round]:
                tmo_high_qc_rounds.append(_tmo_info.high_qc.round)
                tmo_signatures.append(_tmo_info.signature)
            
            tc = Tc.TC(tmo_info.round, tmo_high_qc_rounds, tmo_signatures)
            return tc
        return None

    def advance_round_tc(self, tc):
        if (tc is None) or (tc.round < self._current_round):
            return False
        self._last_round_tc = tc
        self.start_timer(tc.round + 1)
        return True

    def advance_round_qc(self, qc):
        if qc.vote_info.round < self._current_round:
            return False
        self._last_round_tc = None
        self.start_timer(qc.vote_info.round + 1)
        return True
