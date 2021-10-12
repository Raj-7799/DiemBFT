import nacl.hash



import Block as block
import Quorum as qc
import Ledger as ld
from Util import max_round_qc

class PendingBlockTree(dict):

    def __init__(self):
        super()
        self.block_list=dict()
        self.count=0
        
    
    def __setitem__(self, key, value):
        
        # if self["last_node"] is not None:            
        #     self[self["last_node"]]=value
        #     self["last_node"]=value.id #block id to be used for next block insert

        print("insert ",key,value)
        self.count+=1
        if value in self:
            del self[value]            
        super().__setitem__(value,key)
                
        # print("length ",len(self),value,self.count)
        if len(self) == 1:     
            super().__setitem__("root",key)            

    
    def prune(self,id):        
        #use prev root to trace and delete the nodes that not child of id node or id nodes it self        
        super().__setitem__("root",id)

                     
    def add(self,prev_block_id,block):
        self.__setitem__(prev_block_id,block)   


class BlockTree:
    def __init__(self,qc=None,):
        # self._qc = qc.QC(1)
        self._high_qc = qc # highest known QC
        self._pending_votes=None # collected votes per block indexed by their LedgerInfo hash
        self._high_commit_qc=qc # highest QC that serves as a commit certificate        
        self._pending_block_tree=PendingBlockTree()
        self._ledger = ld.Ledger()


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
        msg =  str.encode(str(author)+str(current_round)+str(self.high_qc.vote_info.id)+str(self.high_qc.signatures))
        id = HASHER(msg, encoder=nacl.encoding.HexEncoder)

        new_block = block.Block(author=author,round=current_round,payload=txns,qc=self.high_qc,id=id)
        return new_block
        
    


# compute_block=x.generate_block(1,2)
# print(compute_block)

