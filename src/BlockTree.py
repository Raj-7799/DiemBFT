import Ledger as ld
import Util
from Util import max_round_qc,hash
from collections import defaultdict
import pickle
import client_request as cr

import os
from diembft_logger import get_logger

diem_logger = get_logger(os.path.basename(__file__))


## Creating genesis block for startup 
def create_genesis_object(pvt_key, pbc_key):
    genesis_voteInfo = VoteInfo(id=0,roundNo=-1,parent_id=0,parent_round=-1,exec_state_id=0)
    ledger_commit_info = LedgerCommitInfo(commit_state_id=0,vote_info=genesis_voteInfo)  
    
    genesis_qc = QC(vote_info=genesis_voteInfo,ledger_commit_info=ledger_commit_info, votes=[], author=0, pvt_key=pvt_key, pbc_key=pbc_key)        
    genesis_block =  Block(0, -1, cr.ClientRequest("0", None, pvt_key, pbc_key), genesis_qc, pvt_key, pbc_key)
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
        self.pbc_key             = pbc_key
        self.signature = Util.sign_object_dup(self.signatures, pvt_key)
    
    def __str__(self):
        return "VoteInfo - {} \n LedgerCommitInfo - {} \n author - {}".format(self.vote_info, self.ledger_commit_info, self.author)
    
    def get_signers(self):
        diem_logger.info("[QC][replicaID {}] START get_signers ".format(self.author))
        signers = []
        for voter in self.signatures:
            signers.append(voter)
        diem_logger.info("[QC][replicaID {}] END get_signers ".format(self.author))

        return signers
    
    def verify_self_signature_qc(self):
        return Util.check_authenticity_dup(self.signatures, self.signature, self.pbc_key)

class VoteMsg:
    def __init__(self, vote_info: VoteInfo, ledger_commit_info: LedgerCommitInfo, high_commit_qc: QC, sender: int, pvt_key, pbc_key):
        self.vote_info = vote_info
        self.ledger_commit_info = ledger_commit_info
        self.high_commit_qc = high_commit_qc
        self.sender = sender
        self.signature = Util.sign_object_dup(self.form_signature_object(), pvt_key)

    def verify_self_signature(self, pbc_key):
        return Util.check_authenticity_dup(self.form_signature_object(), self.signature, pbc_key)

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

    def verify_block(self):
        return self.qc.verify_self_signature_qc()

class Node:
    def __init__(self,prev_node_id,block):
        self.prev_node_id = prev_node_id
        self.block = block
        self.childNodes = dict()

class PendingBlockTree:

    def __init__(self,genesis_block, OutputLogger):
        super()
        self.root = Node(0,genesis_block)
        self.OutputLogger = OutputLogger
        self.cache = dict()
        self.cache[genesis_block.id]=self.root
        self.add(genesis_block.id,genesis_block)

        
    def get_node(self,block_id):
        return self.cache[block_id]

    def add(self,prev_node_id,block):
        self.OutputLogger("Block {} added to {} ".format(block.id,prev_node_id))
        node =  self.get_node(prev_node_id)
        node.childNodes[block.id]=Node(prev_node_id,block)
        self.cache[block.id]=node.childNodes[block.id]
    
    def prune(self,id):
        self.OutputLogger("PRUNING {}".format(id))
        self.print_cache()
        curr_node =  self.get_node(id)
        self.root =  curr_node
        self.OutputLogger("new root {}".format(self.root.block.payload))
        self.cache_cleanup(id)
        self.print_cache()

    def cache_cleanup(self,id):
        self.cache=dict()
        self.prune_helper(self.root)
         

    def prune_helper(self,node):
        
        if node is None:
            return 
        self.cache[node.block.id]=node
        for block_id in node.childNodes.keys():
            self.cache[block_id] = node.childNodes[block_id]
            self.prune_helper(node.childNodes[block_id])
        

    def helper(self,temp):
        
        if temp is None:
            return
        self.OutputLogger("helper {}".format(temp.block.payload))
        for i in temp.childNodes.keys():            
            self.OutputLogger("parent node : {} childNode: id {} ,node {} ".format(temp.childNodes[i].prev_node_id,i,temp.childNodes[i].block.payload))
            self.helper(temp.childNodes[i])

    def print_nodes(self):
        temp = self.root
        self.helper(temp)
        
    def print_cache(self):
        self.OutputLogger("PRINTING CACHE ")
        for i in self.cache.keys():
            self.OutputLogger("key {} ,value {} block payload {} ".format(i,self.cache[i],self.cache[i].block.payload))


class BlockTree:
    def __init__(self,fCount,author, pvt_key, pbc_key, memPool, responseHandler, OutputLogger):      
        self._pending_votes=defaultdict(set) # collected votes per block indexed by their LedgerInfo hash
        self.pvt_key = pvt_key
        self.pbc_key = pbc_key
        self.author=author
        self.OutputLogger = OutputLogger

        genesis_qc,genesis_block=create_genesis_object(self.pvt_key, self.pbc_key)
        genesis_block.id=0
        self._high_qc = genesis_qc # highest known QC
        self._high_commit_qc=genesis_qc # highest QC that serves as a commit certificate        
        self._pending_block_tree=PendingBlockTree(genesis_block, self.OutputLogger)
        self._ledger = ld.Ledger(genesis_block, self.author, memPool,self.pending_block_tree, responseHandler, self.OutputLogger)

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
            self.OutputLogger("Leger commit info replicaID {} {}".format(qc.ledger_commit_info.commit_state_id, self.author))
            self._ledger.commit(qc.vote_info.parent_id)
            self.OutputLogger("qc.vote_info.parent_id {} replica {} ".format(qc.vote_info.parent_id,self.author))
            self.pending_block_tree.prune(qc.vote_info.parent_id)
            self._high_commit_qc=max_round_qc(qc,self.high_commit_qc) # max_rond high commit qc ← max round {qc, high commit qc} // max round need elaboration
            
        self._high_qc=max_round_qc(qc,self.high_qc)
        

  
    def execute_and_insert(self,block):
        self._ledger.speculate(block.qc.vote_info.id,block.id,block)
        self.pending_block_tree.add(block.qc.vote_info.id,block)  # forking is possible so we need to know which node to extend

    
    def process_vote(self, vote):

        self.process_qc(vote.high_commit_qc)
        vote_idx = hash(vote.ledger_commit_info)
        self.pending_votes[vote_idx].add(vote)

        if len(self.pending_votes[vote_idx]) == 2 * self.fCount + 1:
            
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
        


