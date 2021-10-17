import TimeoutMsg as timeoutmsg
import TC as Tc
import threading
from collections import defaultdict
from diembft_logger import get_logger
import os
from Pacemaker import Pacemaker
import random
import Util 

diem_logger = get_logger(os.path.basename(__file__))

class PacemakerByz(Pacemaker):
    def __init__(self, safety, blocktree, delta, fCount, replica_broadcast, replicaID, networkByzantineSeed,degreeOfByzantine):
        
        Pacemaker.__init__(self,safety,blocktree,delta,fCount,replica_broadcast,replicaID)

        self.safety = safety
        self.blocktree = blocktree
        self.delta = delta
        self.fCount = fCount
        self.replica_broadcast = replica_broadcast
        self.replicaID = replicaID
        self.current_round = -1
        self.last_round_tc = None
        self.pending_timeouts = defaultdict(set)  #dict of sets of pending timeouts for a round
        self.dict_of_timer = {} # dict of timer for a round
        self.networkByzantineSeed = networkByzantineSeed
        self.degreeOfByzantine=degreeOfByzantine


    def get_round_timer(self):
        value =  Util.get_random(self.networkByzantineSeed,self.degreeOfByzantine)
        print("PaceMakerByz for replicaId {} for random value {}".format(self.replicaID,value))
        if value % 2 == 0:
            return int(self.delta)*100

        return 4 * int(self.delta) // 1000
        