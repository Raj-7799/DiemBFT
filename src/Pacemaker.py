import TimeoutMsg as timeoutmsg
import TC as Tc
import threading
from collections import defaultdict
from diembft_logger import get_logger
import os

diem_logger = get_logger(os.path.basename(__file__))

class Pacemaker:
    def __init__(self, safety, blocktree, delta, fCount, replica_broadcast, replicaID):
        self.safety = safety
        self.blocktree = blocktree
        self.delta = delta
        self.fCount = fCount
        self.replica_broadcast = replica_broadcast
        self.replicaID = replicaID
        self.current_round = 0
        self.last_round_tc = None
        self.pending_timeouts = defaultdict(set)  #dict of sets of pending timeouts for a round
        self.dict_of_timer = {} # dict of timer for a round


    def get_round_timer(self):
        diem_logger.info("[Pacemaker][replicaID {}] START get_round_timer".format(self.replicaID))
        # return 4 * float(int(self.delta)/1000) # Convert Millisecond to second
        return 4 * int(self.delta) // 1000
        

    def _on_timeout(self):
        #self.replica_broadcast(None)
        diem_logger.info("[Pacemaker][replicaID {}] START _on_timeout".format(self.replicaID))
        self.local_timeout_round()

    def _start_timer(self, roundNo):
        diem_logger.info("[Pacemaker][replicaID {}] START _start_timer of roundNo {}".format(self.replicaID, roundNo))
        self.dict_of_timer[roundNo] = threading.Timer(self.get_round_timer(), self._on_timeout)
        self.dict_of_timer[roundNo].start()
        diem_logger.info("[Pacemaker][replicaID {}] END _start_timer of roundNo {}".format(self.replicaID, roundNo))

    def _stop_timer(self, roundNo):
        if roundNo in self.dict_of_timer:
            diem_logger.info("[Pacemaker][replicaID {}] START _stop_timer of roundNo {}".format(self.replicaID, roundNo))
            self.dict_of_timer[roundNo].cancel()

    def start_timer(self, new_round):
        diem_logger.info("[Pacemaker][replicaID {}] START start_timer of new_round {}".format(self.replicaID, new_round))
        self._stop_timer(self.current_round)
        self.current_round = new_round
        self._start_timer(self.current_round)
        diem_logger.info("[Pacemaker][replicaID {}] END start_timer of new_round {}".format(self.replicaID, new_round))

    def local_timeout_round(self):
        diem_logger.info("[Pacemaker][replicaID {}] START local_timeout_round ".format(self.replicaID))
        timeout_info = self.safety.make_timeout(self.current_round, self.blocktree.high_qc, self.last_round_tc)
        timeout_msg = timeoutmsg.TimeoutMsg(timeout_info, self.last_round_tc, self.blocktree.high_qc)
        self.replica_broadcast(timeout_msg)
        diem_logger.info("[Pacemaker][replicaID {}] END local_timeout_round ".format(self.replicaID))

    def _check_if_sender_pending(self, sender, tmo_info):
        diem_logger.info("[Pacemaker][replicaID {}] START _check_if_sender_pending of sender {} of tmo_info.roundNo {}".format(self.replicaID, sender, tmo_info.roundNo))
        for pending_tmo_info in self.pending_timeouts[tmo_info.roundNo]:
            if sender == pending_tmo_info.sender:
                return True
        diem_logger.info("[Pacemaker][replicaID {}] END _check_if_sender_pending of sender {} of tmo_info.roundNo {}".format(self.replicaID, sender, tmo_info.roundNo))
        return False

    def process_remote_timeout(self, tmo):
        diem_logger.info("[Pacemaker][replicaID {}] START process_remote_timeout of tmo.tmo_info.roundNo {}".format(self.replicaID, tmo.tmo_info.roundNo))
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
            diem_logger.info("[Pacemaker][replicaID {}] END process_remote_timeout of tmo.tmo_info.roundNo {} with tc {}".format(self.replicaID, tmo.tmo_info.roundNo, tc.roundNo))
            return tc
        diem_logger.info("[Pacemaker][replicaID {}] END process_remote_timeout of tmo.tmo_info.roundNo {}".format(self.replicaID, tmo.tmo_info.roundNo))
        return None

    def advance_round_tc(self, tc):
        diem_logger.info("[Pacemaker][replicaID {}] START advance_round_tc of self.current_round {}".format(self.replicaID, self.current_round))
        if (tc is None) or (tc.roundNo < self.current_round):
            diem_logger.info("[Pacemaker][replicaID {}] END advance_round_tc ".format(self.replicaID))
            return False
        self.last_round_tc = tc
        self.start_timer(tc.roundNo + 1)
        diem_logger.info("[Pacemaker][replicaID {}] END advance_round_tc of tc.roundNo {}".format(self.replicaID, tc.roundNo))
        return True

    def advance_round_qc(self, qc):
        diem_logger.info("[Pacemaker][replicaID {}] START advance_round_qc of self.current_round {} of qc {}".format(self.replicaID, self.current_round, qc.vote_info.roundNo))
        if qc.vote_info.roundNo < self.current_round:
            diem_logger.info("[Pacemaker][replicaID {}] END advance_round_qc of self.current_round {} of qc {}".format(self.replicaID, self.current_round, qc.vote_info.roundNo))
            return False
        self.last_round_tc = None
        self.start_timer(qc.vote_info.roundNo + 1)
        diem_logger.info("[Pacemaker][replicaID {}] END advance_round_qc of self.current_round {} of qc {}".format(self.replicaID, self.current_round, qc.vote_info.roundNo))
        return True
