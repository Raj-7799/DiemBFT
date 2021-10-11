import nacl.hash
from quorum import QC as qc
import blockchain as block


from blockchain import Block as block
from certificates.quorum import Quorum as qc
from blockchain import Ledger
from util import max_round_qc

class PendingBlockTree(dict):

    def __init__(self):
        super()
        self.block_list=dict()
        
    
    def __setitem__(self, key, value):
        
        # if self["last_node"] is not None:            
        #     self[self["last_node"]]=value
        #     self["last_node"]=value.id #block id to be used for next block insert



        if value in self:
            del self[value]            
        super().__setitem__(value,key)
                
        
        if len(self) == 1:
            for key in self.keys():
                self["root"]=self[key]  

    
    def prune(self,id):        
        #use prev root to trace and delete the nodes that not child of id node or id nodes it self        
        self["root"]=id
                     

        

    def add(self,prev_block_id,block):
        self[block]=prev_block_id

class BlockTree:
    def __init__(self):
        self._qc = qc.QC(1)
        self._high_qc = qc.QC(1) # highest known QC
        self._pending_votes=None # collected votes per block indexed by their LedgerInfo hash
        self._high_commit_qc=qc.QC(1) # highest QC that serves as a commit certificate
        self._pending_block_tree = dict() # tree of blocks pending commitment
        self._pending_block_tree=PendingBlockTree()


    @property
    def pending_block_tree(self):
        return self._pending_block_tree
    
     
        
    @property
    def qc(self):
        return self._qc

    
    @property
    def high_qc(self):
        return self._high_qc
    
    @property
    def pending_votes(self):
        return self._pending_votes
    
    @property
    def high_commit_qc(self):
        return self._high_commit_qc

    def process_qc(self,qc):
        if qc['ledger_commit_info']['commit_state_id'] != None:
            Ledger.commit(qc['vote_info']['parent_id'])
            self.pending_block_tree.prune(qc['vote']['parent_id'])
            self.high_commit_qc=max_round_qc(qc,self.high_commit_qc) # max_rond high commit qc ← max round {qc, high commit qc} // max round need elaboration
        #high qc ← max round {qc, high qc}
        self.high_qc=max_round_qc(qc,self.high_qc)

  
    def execute_and_insert(self,block):
        Ledger.speculate(block.qc.block_id,block.id,block.payload)
        self.pending_block_tree.add(block.qc.block_id,block)  # forking is possible so we need to know which node to extend
    
    def process_vote(self,vote):
        self.process_qc(vote.high_commit_qc)
        vote_idx = hash(vote.ledger_commit_info)
        self.pending_votes[vote_idx].append(vote.signature)

        if len(self.pending_votes[vote_idx])== 4:            
            self.qc = qc.QC(
                vote_info=vote.vote_info,
                ledger_commit_info=vote.ledger_commit_info,
                votes=self.pending_votes
                )
            return self.qc
        return None

    def generate_block(self,txns,current_round):
        author=0
        HASHER = nacl.hash.sha256
        msg =  str.encode(str(author)+str(current_round)+str(self.qc.vote_info.id)+str(self.qc.signature))
        id = HASHER(msg, encoder=nacl.encoding.HexEncoder)

        new_block = block.Block(author=author,round=current_round,payload=txns,qc=self.high_qc,id=id)
        return new_block
        
    


# compute_block=x.generate_block(1,2)
# print(compute_block)

