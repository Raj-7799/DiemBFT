import nacl.hash



import Block as block
import Quorum as qc
import Ledger as ld
from Util import max_round_qc,hash
from diembft_logger import get_logger
from collections import defaultdict
logger = get_logger("blocktree")


class PendingBlockTree(dict):

    def __init__(self,genesis_block):
        logger.debug("PendingBlockTree START: init")
        super()
        #self.block_list=dict()
        # self.count=0
        self.add(genesis_block.id,genesis_block)
        logger.debug("PendingBlockTree END: init")
        
        
    
    def __setitem__(self, key, value):
        logger.debug("PendingBlockTree START: __setitem__",key)
        # if self["last_node"] is not None:            
        #     self[self["last_node"]]=value
        #     self["last_node"]=value.id #block id to be used for next block insert

        print("insert ",key,value)
        # self.count+=1
        if value in self:
            del self[value]            
        super().__setitem__(value,key)
                
        # print("length ",len(self),value,self.count)
        if len(self) == 1:     
            super().__setitem__("root",key)       

        logger.debug("PendingBlockTree END: __setitem__",key)     

    
    def prune(self,id):        
        #use prev root to trace and delete the nodes that not child of id node or id nodes it self    
        logger.debug("PendingBlockTree END: prune   {}".format(key))         
        super().__setitem__("root",id)

                     
    def add(self,prev_block_id,block):
        self.__setitem__(prev_block_id,block)   


class BlockTree:
    def __init__(self,genesis_qc,genesis_block,fCount,author):
        # self._qc = qc.QC(1)
        self._high_qc = qc # highest known QC
        self._pending_votes=defaultdict(set) # collected votes per block indexed by their LedgerInfo hash
        self._high_commit_qc=genesis_qc # highest QC that serves as a commit certificate        
        self._pending_block_tree=PendingBlockTree(genesis_block)
        self._ledger = ld.Ledger(genesis_block)
        self.fCount=fCount
        self.author=author


    @property
    def pending_block_tree(self):
        return self._pending_block_tree
    
     
        
    # @property
    # def qc(self):
    #     return self._qc

    
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
        if qc.ledger_commit_info.commit_state_id != None:
            #Ledger.commit(qc['vote_info']['parent_id'])
            self._ledger.commit(qc.vote_info.parent_id)
            self.pending_block_tree.prune(qc.vote_info.parent_id)
            self._high_commit_qc=max_round_qc(qc,self.high_commit_qc) # max_rond high commit qc ← max round {qc, high commit qc} // max round need elaboration
        #high qc ← max round {qc, high qc}
        self._high_qc=max_round_qc(qc,self.high_qc)

  
    def execute_and_insert(self,block):
        ##In paper : Ledger.speculate(b.qc.block id, b.id, b.payload)
        ## changes:  parameter 1:b.qc.block id <-- is wrong ,parent node is needed extend then new node 
        self._ledger.speculate(block.qc.vote_info.parent_id,block.id,block.payload)
        self.pending_block_tree.add(block.qc.vote_info.parent_id,block)  # forking is possible so we need to know which node to extend
    

    
    def process_vote(self,vote):
        self.process_qc(vote.high_commit_qc)
        vote_idx = hash(vote.ledger_commit_info)
        self.pending_votes[vote_idx].add(vote.signature)

        if len(self.pending_votes[vote_idx])== 3*self.fCount+1:            
            self.qc = qc.QC(
                vote_info=vote.vote_info,
                ledger_commit_info=vote.ledger_commit_info,
                votes=self.pending_votes
                )
            return self.qc
        return None

    def generate_block(self,txns,current_round):        
        new_block = block.Block(
                                    author=self.author,
                                    round=current_round,
                                    payload=txns,
                                    qc=self.high_qc                                    
                                )
                                
        return new_block
        
    


# compute_block=x.generate_block(1,2)
# print(compute_block)

