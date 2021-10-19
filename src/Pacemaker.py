import TimeoutMsg as timeoutmsg
import TC as Tc
import threading
from collections import defaultdict
import time
import os


class Pacemaker:
    def __init__(self, safety, blocktree, delta, fCount, replica_broadcast, replicaID,OutputLogger):
        self.safety = safety
        self.blocktree = blocktree
        self.delta = delta
        self.fCount = fCount
        self.replica_broadcast = replica_broadcast
        self.replicaID = replicaID
        self.current_round = -1 # // Initially zero, we have set it to -1 in to sync with the gensis block round 
        self.last_round_tc = None # / Initially ⊥
        self.pending_timeouts = defaultdict(set)  #dict of sets of pending timeouts for a round
        self.dict_of_timer = {} # dict of timer for a round
        self.OutputLogger=OutputLogger
        self.OutputLogger("__init__")


    def get_round_timer(self):
        #Psuedo code
        # // For example, use 4 ×∆ or α + βcommit gap(r) if ∆ is unknown.
        return 4 * int(self.delta) // 1000 
        
 
    def _on_timeout(self):
        self.local_timeout_round()

    def _start_timer(self, roundNo):
        self.OutputLogger("[_start_timer] Starting timer for round {} max_time : self.get_round_timer() {} timestamp {}".format( roundNo,self.get_round_timer(),time.time()))
        self.dict_of_timer[roundNo] = threading.Timer(self.get_round_timer(), self._on_timeout)
        self.dict_of_timer[roundNo].start()

    def _stop_timer(self, roundNo):
        self.OutputLogger("[_stop_timer] Entry for round {}".format(roundNo))
        if roundNo in self.dict_of_timer:
            self.OutputLogger(" Stopping timer for roundNo {} timestamp {} ".format( roundNo,time.time()))
            self.dict_of_timer[roundNo].cancel()
        self.OutputLogger("[_stop_timer] Exit for round {}".format(roundNo))


    def start_timer(self, new_round):
        self.OutputLogger("[start_timer] Entry for round {}".format(self.current_round))

        self._stop_timer(self.current_round)
        self.OutputLogger("[Updating current_round {} to new_round {}".format( self.current_round, new_round))
        self.current_round = new_round
        self._start_timer(self.current_round)
        self.OutputLogger("[start_timer] Exit for round {}".format(self.current_round))

    def local_timeout_round(self):
        self.OutputLogger("[local_timeout_round] Entry for round {}".format(self.current_round))
        #Psuedo code
        # timeout info ←Safety.make timeout(current round,Block-Tree.high qc,last round tc
        timeout_info = self.safety.make_timeout(self.current_round, self.blocktree.high_qc, self.last_round_tc)
        self.OutputLogger("[local_timeout_round] Local Timeout round called at round {} ".format( self.current_round))
        timeout_msg = timeoutmsg.TimeoutMsg(timeout_info, self.last_round_tc, self.blocktree.high_qc)
        #Psuedo code
        #broadcast TimeoutMsg〈timeout info,last round tc,Block-Tree.high commit qc〉
        self.replica_broadcast(timeout_msg)

        self.OutputLogger("[local_timeout_round] timeout_info {} last_round_tc {} blocktree.high_qc {}".format(timeout_info,self.last_round_tc,self.blocktree.high_qc))
        self.OutputLogger("[local_timeout_round] Exit for round {} broadcasting timeout message timestamp {}".format(self.current_round,timeout_msg,time.time()))


    def _check_if_sender_pending(self, sender, tmo_info):
        for pending_tmo_info in self.pending_timeouts[tmo_info.roundNo]:
            if sender == pending_tmo_info.sender:
                self.OutputLogger("[_check_if_sender_pending] Sender is pending {} of tmo_info.roundNo {}".format( sender, tmo_info.roundNo))
                return True
        self.OutputLogger("[_check_if_sender_pending] Sender {} is not pending for tmo_info.roundNo {}".format( sender, tmo_info.roundNo))
        return False

    def process_remote_timeout(self, tmo):
        self.OutputLogger("[process_remote_timeout] Entry for round {}".format(self.current_round))
        self.OutputLogger(" START process_remote_timeout of tmo.tmo_info.roundNo {}".format( tmo.tmo_info.roundNo))
        # tmo info ←tmo.tmo info
        tmo_info = tmo.tmo_info
        if tmo_info.roundNo < self.current_round:
            return None
        #Psuedo code
        # if tmo info.sender 6∈pending timeouts[tmo info.round].senders then
        #     pending timeouts[tmo info.round] ←pending timeouts[tmo info.round] ∪{tmo info}
        if not self._check_if_sender_pending(tmo_info.sender, tmo_info):
            self.pending_timeouts[tmo_info.roundNo].add(tmo_info)
        #Psuedo code
        # if |pending timeouts[tmo info.round].senders|== f + 1 then
        #     stop timer(current round)
        #     local timeout round() // Bracha timeout
        if len(self.pending_timeouts[tmo_info.roundNo]) == self.fCount + 1:
            self._stop_timer(self.current_round)
            self.local_timeout_round()  #  Bracha timeout
        #Psuedo code
        #if |pending timeouts[tmo info.round].senders|== 2f + 1 then
            # return TC 〈
            # round ←tmo info.round,
            # tmo high qc rounds ←{t.high qc.round |t ∈pending timeouts[tmo info.round]},
            # signatures ←{t.signature |t ∈pending timeouts[tmo info.round]}〉)
        if len(self.pending_timeouts[tmo_info.roundNo]) == (2 * self.fCount) + 1:
            tmo_high_qc_rounds = []
            tmo_signatures = []
            for _tmo_info in list(self.pending_timeouts[tmo_info.roundNo]):
                tmo_high_qc_rounds.append(_tmo_info.high_qc.vote_info.roundNo)
                tmo_signatures.append(_tmo_info.signature)
            
            tc = Tc.TC(tmo_info.roundNo, tmo_high_qc_rounds, tmo_signatures, self.blocktree.pvt_key, self.blocktree.pbc_key)
            self.OutputLogger("[process_remote_timeout] Exit for round {} returning TC tmo.tmo_info.roundNo {} with tc {}".format(self.current_round,tmo.tmo_info.roundNo, tc.roundNo))
            return tc
        self.OutputLogger("[advance_round_tc] END tmo.tmo_info.roundNo {}".format( tmo.tmo_info.roundNo))
        self.OutputLogger("[process_remote_timeout] Exit for round {} returning None".format(self.current_round))

        return None

    def advance_round_tc(self, tc):
        self.OutputLogger("[advance_round_tc] Entry for round {}".format(self.current_round))
        #if tc = ⊥∨tc.round < current round then
        if (tc is None) or (tc.roundNo < self.current_round):
            self.OutputLogger("[advance_round_tc] Either tc is None {}  or self.current_round {}".format( tc, self.current_round))
            return False
        #Psuedo code 
        # last round tc ←tc
        # start timer(tc.round + 1
        self.last_round_tc = tc
        self.start_timer(tc.roundNo + 1)
        self.OutputLogger("[advance_round_tc] Exit for round {} returning true".format(self.current_round))
        return True

    def advance_round_qc(self, qc):
        self.OutputLogger("[advance_round_qc] Entry for round {}".format(self.current_round))
        self.OutputLogger("[advance_round_tc] Attempting to advance round for qc {} from {}".format( qc.vote_info.roundNo, self.current_round))
        #Psuedo code 
        #if qc.vote info.round < current round then
        if qc.vote_info.roundNo < self.current_round:
            self.OutputLogger("[advance_round_tc] VoteInfo round {} is less than current round {}".format( qc.vote_info.roundNo, self.current_round))
            return False
        #Psuedo code 
        #last round tc ←⊥
        self.last_round_tc = None
        ##Psuedo code 
        #start timer(qc.vote info.round + 1
        self.start_timer(qc.vote_info.roundNo + 1)
        self.OutputLogger("[advance_round_qc] Exit for round {} returning True".format(self.current_round))
        return True
