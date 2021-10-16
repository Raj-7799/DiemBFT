import Ledger as ld
import Util
from Util import max_round_qc,hash
from collections import defaultdict
import pickle

import os
from diembft_logger import get_logger

diem_logger = get_logger(os.path.basename(__file__))


## Creating genesis block for startup 
def create_genesis_object(pvt_key, pbc_key):
    genesis_voteInfo = VoteInfo(id=0,roundNo=-1,parent_id=0,parent_round=-1,exec_state_id=0)
    ledger_commit_info = LedgerCommitInfo(commit_state_id=0,vote_info=genesis_voteInfo)  
    
    genesis_qc = QC(vote_info=genesis_voteInfo,ledger_commit_info=ledger_commit_info, votes=[], author=0, pvt_key=pvt_key, pbc_key=pbc_key)        
    genesis_block =  Block(0, -1, "genesis",genesis_qc, pvt_key, pbc_key)
    genesis_block.id = 0

    return genesis_qc , genesis_block


class VoteInfo:
    def __init__(self, id: str, roundNo: int, parent_id: str, parent_round: int, exec_state_id: str):
        self.id = id
        self.roundNo = roundNo
        self.parent_id = parent_id
        self.parent_round = parent_round
        self.exec_state_id = exec_state_id
    
    def __str__(self):
        return "ID - {} \n RoundNo - {} \n ParentID - {} \n ParentRound - {} \n ExecStateID - {}".format(self.id, self.roundNo, self.parent_id, self.parent_round, self.exec_state_id)


class LedgerCommitInfo:
    def __init__(self, commit_state_id: str, vote_info: VoteInfo):
        self.commit_state_id = commit_state_id
        self.vote_info_hash = Util.hash(vote_info)
    

class QC:
    def __init__(self,vote_info :VoteInfo, ledger_commit_info :LedgerCommitInfo, votes, author:int, pvt_key, pbc_key):
        self.vote_info          = vote_info
        self.ledger_commit_info = ledger_commit_info
        self.signatures         = votes
        self.author             = author
        self.signature          = Util.sign_object(self.signatures, pvt_key, pbc_key)
    
    def __str__(self):
        return "VoteInfo - {} \n LedgerCommitInfo - {} \n author - {}".format(self.vote_info, self.ledger_commit_info, self.author)
    
    def get_signers(self):
        diem_logger.info("[QC][replicaID {}] START get_signers ".format(self.author))
        signers = []
        for voter in self.signatures:
            signers.append(voter)
        diem_logger.info("[QC][replicaID {}] END get_signers ".format(self.author))

        return signers

class VoteMsg:
    def __init__(self, vote_info: VoteInfo, ledger_commit_info: LedgerCommitInfo, high_commit_qc: QC, sender: int, pvt_key, pbc_key):
        self.vote_info = vote_info
        self.ledger_commit_info = ledger_commit_info
        self.high_commit_qc = high_commit_qc
        self.sender = sender
        self.signature = Util.sign_object(self.form_signature_object(), pvt_key, pbc_key)
        
    def verify_self_signature(self):

        return Util.check_authenticity(self.form_signature_object(), self.signature)

    def form_signature_object(self):
        return [self.ledger_commit_info]
    
    def __str__(self):
        return "{} ".format(self.sender)


class Block:
    def __init__(self, author: int, roundNo: int, payload: str, qc: QC, pvt_key, pbc_key):
        self.author=author
        self.roundNo=roundNo
        self.payload=payload
        self.qc = qc 
        self.id = Util.hash(pickle.dumps(self.get_block_identity_object()))
    
    def get_block_identity_object(self):
        return [self.author, self.roundNo, self.payload, self.qc.vote_info.id, self.qc.signatures]
    
    def __str__(self):
        return " Block ID - {} \n Payload- {} \n Author - {} \n Round- {} \n QC- {}".format(self.id, self.payload, self.author, self.roundNo, self.qc)

class PendingBlockTree(dict):

    def __init__(self,genesis_block):
        super()

        self.add(genesis_block.id,genesis_block)
        
        
    
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
    def __init__(self,fCount,author, pvt_key, pbc_key, memPool):      
        self._pending_votes=defaultdict(set) # collected votes per block indexed by their LedgerInfo hash
        self.pvt_key = pvt_key
        self.pbc_key = pbc_key
        self.author=author

        genesis_qc,genesis_block=create_genesis_object(self.pvt_key, self.pbc_key)
        genesis_block.id=0
        self._ledger = ld.Ledger(genesis_block, self.author, memPool)
        self._high_qc = genesis_qc # highest known QC
        self._high_commit_qc=genesis_qc # highest QC that serves as a commit certificate        
        self._pending_block_tree=PendingBlockTree(genesis_block)
        self.fCount=fCount


    @property
    def pending_block_tree(self):
        return self._pending_block_tree
    
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
            print("Leger commit info replicaID {} {}".format(qc.ledger_commit_info.commit_state_id, self.author))
            self._ledger.commit(qc.vote_info.parent_id)
            self.pending_block_tree.prune(qc.vote_info.parent_id)
            # print("[BlockTree][replicaID {}] Before HighCommitQC with commit id new QC {} current high commit {}".format(self.author, qc, self._high_commit_qc))
            self._high_commit_qc=max_round_qc(qc,self.high_commit_qc) # max_rond high commit qc ← max round {qc, high commit qc} // max round need elaboration
            # print("[BlockTree][replicaID {}] HighCommitQC with commit id new QC {} current high commit {}".format(self.author, qc, self._high_commit_qc))
        #high qc ← max round {qc, high qc}
        self._high_qc=max_round_qc(qc,self.high_qc)
        # print("[BlockTree][replicaID {}] HighQC with commit id new QC {} current high commit {}".format(self.author, qc, self._high_qc))
        # print("[BlockTree][replicaID {}] END process_qc ".format(self.author))


  
    def execute_and_insert(self,block):
        ##In paper : Ledger.speculate(b.qc.block id, b.id, b.payload)
        ## changes:  parameter 1:b.qc.block id <-- is wrong ,parent node is needed extend then new node 
        self._ledger.speculate(block.qc.vote_info.id,block.id,block)
        self.pending_block_tree.add(block.qc.vote_info.id,block)  # forking is possible so we need to know which node to extend

    
    def process_vote(self, vote):

        self.process_qc(vote.high_commit_qc)
        vote_idx = hash(vote.ledger_commit_info)
        self.pending_votes[vote_idx].add(vote)

        if len(self.pending_votes[vote_idx]) == 2 * self.fCount + 1:
            # print("Forming qc at {}".format(self.author))
            voters = [x.sender for x in self.pending_votes[vote_idx]]

            qc = QC(
                vote_info=vote.vote_info,
                ledger_commit_info=vote.ledger_commit_info,
                votes= voters,
                author=self.author,
                pvt_key=self.pvt_key,
                pbc_key=self.pbc_key
            )
            
            return qc
        
        diem_logger.info("Could not form qc for vote msg at replica {}. Vote count {} ".format(self.author, len(self.pending_votes[vote_idx])))
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

