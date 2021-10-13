import Ledger as ld
import Util
from Util import max_round_qc,hash
from diembft_logger import get_logger
from collections import defaultdict
logger = get_logger("blocktree")

## Creating genesis block for startup 
def create_genesis_object(pvt_key, pbc_key):
    genesis_voteInfo = VoteInfo(id=0,roundNo=0,parent_id=0,parent_round=0,exec_state_id=0)
    ledger_commit_info = LedgerCommitInfo(commit_state_id=0,vote_info=genesis_voteInfo)  
    
    genesis_qc = QC(vote_info=genesis_voteInfo,ledger_commit_info=ledger_commit_info, votes=[], author=0, pvt_key=pvt_key, pbc_key=pbc_key)        
    genesis_block =  Block(0,0,"genesis",genesis_qc, pvt_key, pbc_key)
    
    return genesis_qc , genesis_block


class VoteInfo:
    def __init__(self, id: str, roundNo: int, parent_id: str, parent_round: int, exec_state_id: str):
        self.id = id
        self.roundNo = roundNo
        self.parent_id = parent_id
        self.parent_round = parent_round
        self.exec_state_id = exec_state_id


class LedgerCommitInfo:
    def __init__(self, commit_state_id: str, vote_info: VoteInfo):
        self.commit_state_id = commit_state_id
        self.vote_info_hash = Util.hash(vote_info)

class QC():
    def __init__(self,vote_info :VoteInfo, ledger_commit_info :LedgerCommitInfo, votes, author:int, pvt_key, pbc_key):
        self.vote_info          = vote_info
        self.ledger_commit_info = ledger_commit_info
        self.signatures         = votes
        self.author             = author
        self.signature          = Util.sign_object(self.signatures, pvt_key, pbc_key)
    
    def get_signers(self):
        signers = []
        for voter in self.signatures:
            signers.append(voter.sender)
        
        return signers

class VoteMsg:
    def __init__(self, vote_info: VoteInfo, ledger_commit_info: LedgerCommitInfo, high_commit_qc: QC, sender: int, pvt_key, pbc_key):
        self.vote_info = vote_info
        self.ledger_commit_info = ledger_commit_info
        self.high_commit_qc = high_commit_qc
        self.sender = sender
        self.signature = Util.sign_object(self.form_signature_object(), pvt_key, pbc_key)#key.sign_message(self._ledger_commit_info) 
        
    def verify_self_signature(self):
        return Util.check_authenticity(self.form_signature_object(), self.signature)

    def form_signature_object(self):
        return [self.ledger_commit_info]


class Block:
    def __init__(self, author: int, roundNo: int, payload: str, qc: QC, pvt_key, pbc_key):
        self.author=author
        self.roundNo=roundNo
        self.payload=payload
        self.qc = qc 
        self.id = Util.sign_object(self.get_block_identity_object(), pvt_key, pbc_key)
    
    def get_block_identity_object(self):
        return [self.author, self.roundNo, self.payload, self.qc.vote_info.id, self.qc.signatures]

class PendingBlockTree(dict):

    def __init__(self,genesis_block):
        #logger.debug("PendingBlockTree START: init")
        super()

        self.add(genesis_block.id,genesis_block)
        #logger.debug("PendingBlockTree END: init")
        
        
    
    def __setitem__(self, key, value):
        # #logger.debug("PendingBlockTree START: __setitem__",key)
        
        if value in self:
            del self[value]            
        super().__setitem__(value,key)
                        
        if len(self) == 1:     
            super().__setitem__("root",key)       

        # #logger.debug("PendingBlockTree END: __setitem__",key)     

    
    def prune(self,id):        
        #use prev root to trace and delete the nodes that not child of id node or id nodes it self    
        # #logger.debug("PendingBlockTree START: prune  ")         
        super().__setitem__("root",id)
        # #logger.debug("PendingBlockTree EMD: prune  ")      

                     
    def add(self,prev_block_id,block):
        self.__setitem__(prev_block_id,block)   


class BlockTree:
    def __init__(self,fCount,author, pvt_key, pbc_key):        
        self._pending_votes=defaultdict(set) # collected votes per block indexed by their LedgerInfo hash
        self.pvt_key = pvt_key
        self.pbc_key = pbc_key
        genesis_qc,genesis_block=create_genesis_object(self.pvt_key, self.pbc_key)
        self._high_qc = genesis_qc # highest known QC
        self._high_commit_qc=genesis_qc # highest QC that serves as a commit certificate        
        self._pending_block_tree=PendingBlockTree(genesis_block)
        self.author=author
        self._ledger = ld.Ledger(genesis_block, self.author)
        self.fCount=fCount


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
    

    
    def process_vote(self, vote):
        self.process_qc(vote.high_commit_qc)
        vote_idx = hash(vote.ledger_commit_info)
        self.pending_votes[vote_idx].add(vote.signature)

        if len(self.pending_votes[vote_idx])== 2*self.fCount+1:            
            self.qc = QC(
                vote_info=vote.vote_info,
                ledger_commit_info=vote.ledger_commit_info,
                votes=self.pending_votes
                )
            return self.qc
        return None

    def generate_block(self,txns,current_round):        
        new_block = Block(
                                    author=self.author,
                                    roundNo=current_round,
                                    payload=txns,
                                    qc=self.high_qc,
                                    pvt_key=self.pvt_key,
                                    pbc_key=self.pbc_key
                                )

        return new_block
        
        ## Creating genesis block for startup 
# compute_block=x.generate_block(1,2)
# print(compute_block)

