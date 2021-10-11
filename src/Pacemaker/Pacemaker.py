

import time
from Messages import TimeoutMsg


class Pacemaker:

    def __init__(self, safety, blocktree, replica):  # delta and f can be taken from config
        self._safety = safety
        self._replica = replica
        self._current_round = 0
        self._last_round_tc = None
        self._pending_timeouts = None

    def get_round_timer(self, r, delta):
        return 4 * self.replica.tDelta

    def _start_timer(self, round):
        pass  # self._dict_of_timer[round] = new

    def _stop_timer(self, round):
        pass

    def start_timer(self, new_round):
        self.stop_timer(self._current_round)
        self._current_round = new_round
        self._start_timer(round)

    def local_timeout_round(self):
        timeout_info = self._safety.make_timeout(self._current_round, self._blocktree.high_qc, self._last_round_tc)
        timeout_msg = TimeoutMsg()
        timeout_msg.tmo_info = timeout_info
        timeout_msg.last_round_tc = timeout_info

    def _check_if_sender_pending(self, sender):
        for pending_tmo_info in self._pending_timeouts[tmo_info.round]:
            if sender == pending_tmo_info.sender:
                return True
        return False

    def process_remote_timeout(self, tmo):
        tmo_info = tmo.tmo_info
        if tmo_info.round < current_round:
            return None
        if not _check_if_sender_pending(tmo_info.sender):
            self._pending_timeouts[tmo_info.round].append(tmo_info)
        if len(self._pending_timeouts[tmo_info.round]) == self._replica.fCount + 1:
            self._stop_timer(self._current_round)
            #  local_timeout_round
        if len(self._pending_timeouts[tmo_info.round]) == (2 * self._replica.fCount) + 1:
            tc = TC()
            tc.round = tmo_info.round
            tc.tmo_high_qc_rounds = None  # currently I don't understand what is t
            tc.signatures = None  # currently I don't understand what is t
            return tc
        return None

    def advance_round_tc(self, tc):
        if (tc is None) or (tc.round < self._current_round):
            return False
        self._last_round_tc = tc
        self._start_timer(tc.round + 1)
        return True

    def advance_round_qc(self, qc):
        if qc.vote_info.round < self._current_round:
            return False
        self._last_round_tc = None
        self._start_timer(qc.vote_info.round + 1)
        return True
