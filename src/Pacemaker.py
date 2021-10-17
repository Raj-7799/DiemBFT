import TimeoutMsg as timeoutmsg
import TC as Tc
import threading
from collections import defaultdict
from diembft_logger import get_logger
import os

diem_logger = get_logger(os.path.basename(__file__))

class Pacemaker:
    def __init__(self, safety, blocktree, delta, fCount, replica_broadcast, replicaID, memPool):
        self.safety = safety
        self.blocktree = blocktree
        self.delta = delta
        self.fCount = fCount
        self.replica_broadcast = replica_broadcast
        self.replicaID = replicaID
        self.memPool = memPool
        self.current_round = -1
        self.last_round_tc = None
        self.pending_timeouts = defaultdict(set)  #dict of sets of pending timeouts for a round
        self.dict_of_timer = {} # dict of timer for a round


    def get_round_timer(self):
        return 4 * int(self.delta) // 1000
        

    def _on_timeout(self):
        self.local_timeout_round()

    def _start_timer(self, roundNo):
        if(self.memPool.safe_to_start_timer()):
            print("[Pacemaker][replicaID {}] Starting timer for round {}".format(self.replicaID, roundNo))
            self.dict_of_timer[roundNo] = threading.Timer(self.get_round_timer(), self._on_timeout)
            self.dict_of_timer[roundNo].start()
        else:
            print("Pacemaker not starting Timer")

    def _stop_timer(self, roundNo):
        if roundNo in self.dict_of_timer:
            print("[Pacemaker][replicaID {}] Stopping timer for roundNo {}".format(self.replicaID, roundNo))
            self.dict_of_timer[roundNo].cancel()

    def start_timer(self, new_round):
        self._stop_timer(self.current_round)
        print("[Pacemaker][replicaID {}] Updating current_round {} to new_round {}".format(self.replicaID, self.current_round, new_round))
        self.current_round = new_round
        self._start_timer(self.current_round)

    def local_timeout_round(self):
        timeout_info = self.safety.make_timeout(self.current_round, self.blocktree.high_qc, self.last_round_tc)
        print("[Pacemaker][replicaID {}] Local Timeout round called at round {} ".format(self.replicaID, self.current_round))
        timeout_msg = timeoutmsg.TimeoutMsg(timeout_info, self.last_round_tc, self.blocktree.high_qc)
        self.replica_broadcast(timeout_msg)

    def _check_if_sender_pending(self, sender, tmo_info):
        for pending_tmo_info in self.pending_timeouts[tmo_info.roundNo]:
            if sender == pending_tmo_info.sender:
                print("[Pacemaker][replicaID {}] Sender is pending {} of tmo_info.roundNo {}".format(self.replicaID, sender, tmo_info.roundNo))
                return True
        print("[Pacemaker][replicaID {}] Sender {} is not pending for tmo_info.roundNo {}".format(self.replicaID, sender, tmo_info.roundNo))
        return False

    def process_remote_timeout(self, tmo):
        print("[Pacemaker][replicaID {}] START process_remote_timeout of tmo.tmo_info.roundNo {}".format(self.replicaID, tmo.tmo_info.roundNo))
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
            print("[Pacemaker][replicaID {}] END process_remote_timeout of tmo.tmo_info.roundNo {} with tc {}".format(self.replicaID, tmo.tmo_info.roundNo, tc.roundNo))
            return tc
        print("[Pacemaker][replicaID {}] END process_remote_timeout of tmo.tmo_info.roundNo {}".format(self.replicaID, tmo.tmo_info.roundNo))
        return None

    def advance_round_tc(self, tc):
        if (tc is None) or (tc.roundNo < self.current_round):
            print("[Pacemaker][replicaID {}] Either tc is None {}  or self.current_round {}".format(self.replicaID, tc, self.current_round))
            return False
        self.last_round_tc = tc
        self.start_timer(tc.roundNo + 1)
        return True

    def advance_round_qc(self, qc):
        print("[Pacemaker][replicaID {}] Attempting to advance round for qc {} from {}".format(self.replicaID, qc.vote_info.roundNo, self.current_round))
        if qc.vote_info.roundNo < self.current_round:
            print("[Pacemaker][replicaID {}] VoteInfo round {} is less than current round {}".format(self.replicaID, qc.vote_info.roundNo, self.current_round))
            return False
        
        self.last_round_tc = None
        self.start_timer(qc.vote_info.roundNo + 1)
        return True
