from collections import OrderedDict
import random

import os
from diembft_logger import get_logger

diem_logger = get_logger(os.path.basename(__file__))


class LeaderElection:
    def __init__(self, f, paceMaker, ledger, validators, replicaID, OutputLogger):
        self.validators = validators
        self.window_size = f + 1
        self.exclude_size = f + 1
        self.reputation_leaders = {}
        self.paceMaker = paceMaker
        self.ledger = ledger
        self.replicaID = replicaID
        self.OutputLogger = OutputLogger

    def elect_reputation_leaders(self, qc):
        active_validators = OrderedDict()
        last_authors = OrderedDict()
        current_qc = qc
        i = 0

        while i < self.window_size or len(last_authors) < self.exclude_size:
            self.OutputLogger("[replicaID {}] LeaderElection finding for block {}".format(self.replicaID, current_qc.vote_info.parent_id))
            current_block = self.ledger.committed_block(current_qc.vote_info.parent_id)
            # Change if block is the genesis block stop iteration
            if current_block.id == 0:
                break

            block_author = current_block.author

            
            if i < self.window_size:
                signers = current_qc.get_signers()
                for signer in signers:
                    active_validators[signer] = True
            
            if len(last_authors) < self.exclude_size:
                last_authors[block_author] = True
            
            current_qc = current_block.qc
            i += 1
        
        for author in last_authors:
            if author in active_validators:
                del active_validators[author]
        
        active_validators = list(active_validators.keys())
        
        # This is to make sure when proposal fails in very first round we handle it smoothly
        if len(active_validators) == 0:
            return None
        
        random.seed(qc.vote_info.roundNo)
        self.OutputLogger("[replicaID {}] END qc.vote_info.roundNo {}".format(self.replicaID,qc.vote_info.roundNo))
        return active_validators[random.randint(0, len(active_validators) - 1)]

        
    def update_leaders(self, qc):
        self.OutputLogger("[replicaID {}] START qc.vote_info.roundNo {} self.paceMaker.current_round {}".format(self.replicaID, qc.vote_info.roundNo, self.paceMaker.current_round))
        extended_round = qc.vote_info.parent_round
        qc_round = qc.vote_info.roundNo
        current_round = self.paceMaker.current_round

        if extended_round + 1 == qc_round and qc_round + 1 == current_round:
            elected_leader = self.elect_reputation_leaders(qc)
            ##In paper : self.reputation_leaders[current_round + 1]
            ## changes:  if elected_leader is not None:self.reputation_leaders[current_round + 1] = elected_leader 
            ## Incase the very first proposal voting fails, the genesis block will only have one author and no signature
            # This will return no elected_leader
            if elected_leader is not None:
                self.reputation_leaders[current_round + 1] = elected_leader
        self.OutputLogger("[replicaID {}] END qc.vote_info.roundNo {}".format(self.replicaID, qc.vote_info.roundNo))

    
    def get_leader(self, roundNo):
        if roundNo < 0:
            return 0
        self.OutputLogger("[replicaID {}] START roundNo {} self.paceMaker.current_round {}".format(self.replicaID,roundNo, self.paceMaker.current_round))
        if roundNo in self.reputation_leaders:
            self.OutputLogger("[replicaID {}]  repuation_leaders for roundNo {} is {} self.paceMaker.current_round {}".format(self.replicaID,roundNo, self.reputation_leaders[roundNo], self.paceMaker.current_round))
            return self.reputation_leaders[roundNo]
        self.OutputLogger("[replicaID {}] END roundNo {} self.paceMaker.current_round {}".format(self.replicaID, roundNo, self.paceMaker.current_round))
        return self.validators[(roundNo // 2) % len(self.validators)]
