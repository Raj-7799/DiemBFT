from collections import OrderedDict
import random

class LeaderElection:
    def __init__(self, f, replica):
        self.validators = [ r for r in replica.replicaInfos]
        self.window_size = f + 1
        self.exclude_size = f + 1
        self.reputation_leaders = {}
        self.replica = replica

    def elect_reputation_leaders(self, qc):
        active_validators = OrderedDict()
        last_authors = OrderedDict()
        current_qc = qc
        i = 0

        while i < self.window_size or len(last_authors) < self.exclude_size:
            current_block = self.replica.ledger.committed_block(current_qc.vote_info.parent_id)
            block_author = current_block.author
            #TODO:  add some validation for genesis block
            
            if i < self.window_size:
                signers = qc.get_signers()
                for signer in signers:
                    active_validators[signer] = True
            
            if i < self.exclude_size:
                last_authors[block_author] = True
            
            current_qc = current_block.qc
            i += 1
        
        for author in last_authors:
            if author in active_validators:
                del active_validators[author]
        
        active_validators = list(active_validators)
        return active_validators[random.randint(0, len(active_validators - 1))]

        
    def update_leaders(self, qc):
        extended_round = qc.vote_info.parent_round
        qc_round = qc.vote_info.round
        current_round = self.replica.paceMaker.current_round

        if extended_round + 1 == qc_round and qc_round + 1 == current_round:
            self.reputation_leaders[current_round + 1] = self.elect_reputation_leaders(qc)
    
    def get_leader(self, round):
        if round in self.reputation_leaders:
            return self.reputation_leaders[round]
        
        return self.validators[(round // 2) % len(self.validators)]
        
