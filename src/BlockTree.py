import Ledger as ld
import Util
from Util import max_round_qc,hash
from collections import defaultdict
import pickle
import client_request as cr

import os



## Creating genesis block for startup 
def create_genesis_object(pvt_key, pbc_key):
    genesis_voteInfo = VoteInfo(id=0,roundNo=-1,parent_id=0,parent_round=-1,exec_state_id=0)
    ledger_commit_info = LedgerCommitInfo(commit_state_id=0,vote_info=genesis_voteInfo)  
    
    genesis_qc = QC(vote_info=genesis_voteInfo,ledger_commit_info=ledger_commit_info, votes=[], author=0, pvt_key=pvt_key, pbc_key=pbc_key)        
    genesis_block =  Block(0, -1, cr.ClientRequest("0", None, pvt_key), genesis_qc, pvt_key, pbc_key)
    genesis_block.id = 0

    return genesis_qc , genesis_block


class VoteInfo:
    def __init__(self, id: str, roundNo: int, parent_id: str, parent_round: int, exec_state_id: str):
        #// Id and round of block
        self.id = id 
        self.roundNo = roundNo
        #// Id and round of parent
        self.parent_id = parent_id
        self.parent_round = parent_round
        #// Speculated execution state
        self.exec_state_id = exec_state_id
    
    def __str__(self):
        return "VoteInfo :  [ ID - {}  RoundNo - {}  ParentID - {}  ParentRound - {}  ExecStateID - {} ]".format(self.id, self.roundNo, self.parent_id, self.parent_round, self.exec_state_id)


#// speculated new committed state to vote directly on
class LedgerCommitInfo:
    def __init__(self, commit_state_id: str, vote_info: VoteInfo):
        self.commit_state_id = commit_state_id #// ⊥ if no commit happens when this vote is aggregated to Q
        self.vote_info_hash = Util.hash(vote_info) #// Hash of VoteMsg.vote info
    
    def __str__(self):
        return "LedgerCommitInfo :  [ commit_state_id {} vote_info_hash {} ]".format(self.commit_state_id,self.vote_info_hash[0:4])

#// QC is a VoteMsg with multiple signatures
class QC:
    def __init__(self,vote_info :VoteInfo, ledger_commit_info :LedgerCommitInfo, votes, author:int, pvt_key, pbc_key):
        self.vote_info          = vote_info
        self.ledger_commit_info = ledger_commit_info  
        self.signatures         = votes #// A quorum of signatures
        self.author             = author #// QC is a VoteMsg with multiple signatures
        self.pbc_key            = pbc_key
        self.signature = Util.sign_object_dup(self.signatures, pvt_key)
    
    def __str__(self):
        return "QC : [ signature - {} VoteInfo - {}  author - {} ledger_commit_info {} ]".format(self.signature[0:3],self.vote_info, self.author,self.ledger_commit_info)
    
    def get_signers(self):
        signers = []
        for voter in self.signatures:
            signers.append(voter)

        return signers
    
    def verify_self_signature_qc(self):
        return Util.check_authenticity_dup(self.signatures, self.signature, self.pbc_key)


class VoteMsg:
    def __init__(self, vote_info: VoteInfo, ledger_commit_info: LedgerCommitInfo, high_commit_qc: QC, sender: int, pvt_key, pbc_key):
        self.vote_info = vote_info
        self.ledger_commit_info = ledger_commit_info #// Speculated ledger info
        self.high_commit_qc = high_commit_qc #// QC to synchronize on committed blocks
        self.sender = sender #added automatically when constructe
        self.signature = Util.sign_object_dup(self.form_signature_object(), pvt_key) #// Signed automatically when constructed
 

    def verify_self_signature(self, pbc_key):
        return Util.check_authenticity_dup(self.form_signature_object(), self.signature, pbc_key)

    def form_signature_object(self):
        return [self.ledger_commit_info]
    
    def __str__(self):
        return "{} ".format(self.sender)


class Block:
    def __init__(self, author: int, roundNo: int, payload: str, qc: QC, pvt_key, pbc_key):
        self.author=author #// The author of the block, may not be the same as qc.author after view-chang
        self.roundNo=roundNo #// Yhe round that generated this proposal
        self.payload=payload #// Proposed transaction(s)
        self.qc = qc #QC for parent block
        #Psuedo code 
        #id ←hash(author || round || payload || qc.vote info.id || qc.signatures) 
        self.id = Util.hash(pickle.dumps(self.get_block_identity_object()))
    
    def get_block_identity_object(self):
        return [self.author, self.roundNo, self.payload, self.qc.vote_info.id, self.qc.signatures]
    
    def __str__(self):
        return "Block : [Block ID - {}  Payload- {}  Author - {}  Round- {}  QC- {} ]".format(self.id, self.payload, self.author, self.roundNo, self.qc)


class Node:
    def __init__(self,prev_node_id,block):
        self.prev_node_id = prev_node_id
        self.block = block
        self.childNodes = dict()

class PendingBlockTree:

    def __init__(self,genesis_block):
        super()
        self.root = Node(0,genesis_block)
        
        self.cache = dict()
        self.cache[genesis_block.id]=self.root
        self.add(genesis_block.id,genesis_block)
        
    def get_node(self,block_id):
        if block_id in self.cache.keys():
            return self.cache[block_id]
        return None

    def add(self,prev_node_id,block):
        node =  self.get_node(prev_node_id)
        if node is None:
            node=self.root #Correction for forking , will be used in syncing
        node.childNodes[block.id]=Node(prev_node_id,block)
        self.cache[block.id]=node.childNodes[block.id]
    
    def prune(self,id):
        curr_node =  self.get_node(id)
        if curr_node is None:
            return
        self.root =  curr_node
        self.cache_cleanup(id)


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
        

class BlockTree:
    def __init__(self,fCount,author, pvt_key, pbc_key, memPool, responseHandler,send_sync_message,OutputLogger):      
        self._pending_votes=defaultdict(set) # collected votes per block indexed by their LedgerInfo hash
        self.pvt_key = pvt_key
        self.pbc_key = pbc_key
        self.author=author
        self.OutputLogger=OutputLogger

        genesis_qc,genesis_block=create_genesis_object(self.pvt_key, self.pbc_key)
        genesis_block.id=0
        self._high_qc = genesis_qc # highest known QC
        self._high_commit_qc=genesis_qc # highest QC that serves as a commit certificate        
        self._pending_block_tree=PendingBlockTree(genesis_block) #tree of blocks pending commitment, starting node will be gensis until pruned to some other block 
        
        
        self._ledger = ld.Ledger(genesis_block, self.author, memPool,self.pending_block_tree, responseHandler,OutputLogger)

        self.fCount=fCount
        self.send_sync_message=send_sync_message


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
        #Psuedo code
        # if qc.ledger commit info.commit state id 6= ⊥ then
        if qc.ledger_commit_info.commit_state_id != None:
            # Ledger.commit(qc.vote info.parent id
            self._ledger.commit(qc.vote_info.parent_id)
            #pending block tree.prune(qc.vote info.parent id) // parent id becomes the new root of pending
            self.pending_block_tree.prune(qc.vote_info.parent_id)
            self._high_commit_qc=max_round_qc(qc,self.high_commit_qc) # max_rond high commit qc ← max round {qc, high commit qc} // max round need elaboration
    
        #high qc ← max round {qc, high qc}
        self._high_qc=max_round_qc(qc,self.high_qc)
        
    def execute_and_insert(self,block,current_round):
        if block.roundNo >  current_round + 1:
            self.OutputLogger("[execute_and_insert] Syncing required for block.roundNo {} current_round {}".format(block.roundNo,current_round))

            #Sync node 
            self.send_sync_message((self._ledger.last_committed_block,self.replicaID))
        ##In paper : Ledger.speculate(b.qc.block id, b.id, b.payload)
        ## changes:  parameter 1:b.qc.block id <-- is wrong ,parent node is needed extend then new node 
        self._ledger.speculate(block.qc.vote_info.id,block.id,block)
        self.pending_block_tree.add(block.qc.vote_info.id,block)  # forking is possible so we need to know which node to extend
        self.OutputLogger("[execute_and_insert] Inserted block.roundNo {} current_round {} into sepculate and pending block tree".format(block.roundNo,current_round))

    def process_vote(self, vote):
        self.OutputLogger("[process_vote] Entry for vote.roundNo {}".format(vote.vote_info.roundNo))
        #Psuedo code 
        #process qc(v.high commit qc)
        self.process_qc(vote.high_commit_qc)
        #Psuedo code 
        #vote idx ←hash(v.ledger commit info)
        vote_idx = hash(vote.ledger_commit_info)
        #Psuedo code 
        #pending votes[vote idx] ←pending votes[vote idx] ∪v.signatur
        self.pending_votes[vote_idx].add(vote)
        #Psuedo code 
        #if |pending votes[vote idx]|= 2f + 1 then
        if len(self.pending_votes[vote_idx]) == 2 * self.fCount + 1:
            self.OutputLogger("[process_vote] Received 2 * f + 1 votes for round {}".format(vote.vote_info.roundNo))
            voters = [x.sender for x in self.pending_votes[vote_idx]]
            #Psuedo code
                # qc ←QC 〈
                # vote info ←v.vote info,
                # state id ←v.state id,
                # votes ←pending votes[vote idx])
            qc = QC(
                vote_info=vote.vote_info,
                ledger_commit_info=vote.ledger_commit_info,
                votes= voters,
                author=self.author,
                pvt_key=self.pvt_key,
                pbc_key=self.pbc_key
            )

            self.OutputLogger("[process_vote] Formed QC for vote.roundNo {}  with new qc {}".format(vote.vote_info.roundNo, qc))
            return qc
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
        self.OutputLogger("[generate_block] Generated block for round {} with block id {}".format(current_round,new_block.id))    
        return new_block
        
    def start_sync(current_block,block_round):
        self.OutputLogger("[start_sync] Entry for current_block {} and block_round".format(current_round,block_round))    
        last_committed_block =  self.ledger.last_committed_block
        send_sync_message((last_committed_block,self.author))
        self.OutputLogger("[start_sync] Exit for current_block {} and block_round".format(current_round,block_round))    

        


