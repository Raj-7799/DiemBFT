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
    print("START: create_genesis_object ")
    genesis_voteInfo = VoteInfo(id=0,roundNo=0,parent_id=0,parent_round=0,exec_state_id=0)
    ledger_commit_info = LedgerCommitInfo(commit_state_id=0,vote_info=genesis_voteInfo)  
    
    genesis_qc = QC(vote_info=genesis_voteInfo,ledger_commit_info=ledger_commit_info, votes=[], author=0, pvt_key=pvt_key, pbc_key=pbc_key)        
    genesis_block =  Block(0, 0, "genesis",genesis_qc, pvt_key, pbc_key)
    genesis_block.id = 0

    print("END: create_genesis_object ")
    return genesis_qc , genesis_block


class VoteInfo:
    def __init__(self, id: str, roundNo: int, parent_id: str, parent_round: int, exec_state_id: str):
        self.id = id
        self.roundNo = roundNo
        self.parent_id = parent_id
        self.parent_round = parent_round
        self.exec_state_id = exec_state_id
    
    def __str__(self):
        return "ID - {} RoundNo - {} ParentID - {} ParentRound - {} ExecStateID - {}".format(self.id, self.roundNo, self.parent_id, self.parent_round, self.exec_state_id)


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
        return "VoteInfo - {} LedgerCommitInfo - {} author - {}".format(self.vote_info, self.ledger_commit_info, self.author)
    
    def get_signers(self):
        diem_logger.info("[QC][replicaID {}] START get_signers ".format(self.author))
        signers = []
        for voter in self.signatures:
            signers.append(voter.sender)
        diem_logger.info("[QC][replicaID {}] END get_signers ".format(self.author))

        return signers

class VoteMsg:
    def __init__(self, vote_info: VoteInfo, ledger_commit_info: LedgerCommitInfo, high_commit_qc: QC, sender: int, pvt_key, pbc_key):
        self.vote_info = vote_info
        self.ledger_commit_info = ledger_commit_info
        self.high_commit_qc = high_commit_qc
        self.sender = sender
        self.signature = Util.sign_object(self.form_signature_object(), pvt_key, pbc_key)#key.sign_message(self._ledger_commit_info) 
        
    def verify_self_signature(self):
        diem_logger.info("[VoteMsg][replicaID {}] START verify_self_signature ".format(self.author))

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
        return "Block ID - {} Payload- {} Author - {} Round- {} QC- {}".format(self.id, self.payload, self.author, self.roundNo, self.qc)

class Node:
    def __init__(self,prev_node_id,block):
        self.prev_node_id = prev_node_id
        self.block = block
        self.childNodes = dict()

class PendingBlockTree:

    def __init__(self,genesis_block):
        #logger.debug("PendingBlockTree START: init")
        super()
        self.root = Node(0,genesis_block)
        
        self.cache = dict()
        self.cache[genesis_block.id]=self.root
        self.add(genesis_block.id,genesis_block)


        #logger.debug("PendingBlockTree END: init")
        
    def get_node(self,block_id):
        return self.cache[block_id]

    def add(self,prev_node_id,block):
        print("Block {} added to {} ".format(block.id,prev_node_id))
        node =  self.get_node(prev_node_id)
        node.childNodes[block.id]=Node(prev_node_id,block)
        self.cache[block.id]=node.childNodes[block.id]
    
    def prune(self,id):
        curr_node =  self.get_node(id)
        self.root =  curr_node
        print("new root ",self.root.block.payload)
        self.cache_cleanup(id)
        self.print_cache()
        # parent_node = self.get_node(curr_node.prev_node_id)
        # parent_node.childNodes[id]=None
        # del parent_node.childNodes[id]

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
        print("helper ",temp.block.payload)
        for i in temp.childNodes.keys():            
            print("parent node : {} childNode: id {} ,node {} ".format(temp.childNodes[i].prev_node_id,i,temp.childNodes[i].block.payload))
            self.helper(temp.childNodes[i])

    def print_nodes(self):
        temp = self.root
        self.helper(temp)
        
    def print_cache(self):
        print("PRINTING CACHE ")
        for i in self.cache.keys():
            print("key {} ,value {} block payload {} ".format(i,self.cache[i],self.cache[i].block.payload))


class BlockTree:
    def __init__(self,fCount,author, pvt_key, pbc_key):        
        self._pending_votes=defaultdict(set) # collected votes per block indexed by their LedgerInfo hash
        self.pvt_key = pvt_key
        self.pbc_key = pbc_key
        self.author=author

        genesis_qc,genesis_block=create_genesis_object(self.pvt_key, self.pbc_key)
        genesis_block.id=0
        self._high_qc = genesis_qc # highest known QC
        self._high_commit_qc=genesis_qc # highest QC that serves as a commit certificate        
        self._pending_block_tree=PendingBlockTree(genesis_block)
        self._ledger = ld.Ledger(genesis_block, self.author,self.pending_block_tree)

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
        print("[BlockTree][replicaID {}] START process_qc with commit id {}".format(self.author, qc.ledger_commit_info.commit_state_id))

        if qc.ledger_commit_info.commit_state_id != None:
            #Ledger.commit(qc['vote_info']['parent_id'])
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
        print("[BlockTree][replicaID {}] START execute_and_insert  ".format(self.author))

        ##In paper : Ledger.speculate(b.qc.block id, b.id, b.payload)
        ## changes:  parameter 1:b.qc.block id <-- is wrong ,parent node is needed extend then new node 
        self._ledger.speculate(block.qc.vote_info.parent_id,block.id,block.payload)
        self.pending_block_tree.add(block.qc.vote_info.id,block)  # forking is possible so we need to know which node to extend
        print("[BlockTree][replicaID {}] START execute_and_insert  ".format(self.author))

    
    def process_vote(self, vote):
        print("[BlockTree][replicaID {}] START process_vote  ".format(self.author))

        self.process_qc(vote.high_commit_qc)
        vote_idx = hash(vote.ledger_commit_info)
        self.pending_votes[vote_idx].add(vote)

        if len(self.pending_votes[vote_idx])== 2*self.fCount+1:
            # print("Forming qc at {}".format(self.author))
            
            qc = QC(
                vote_info=vote.vote_info,
                ledger_commit_info=vote.ledger_commit_info,
                votes=self.pending_votes[vote_idx],
                author=self.author,
                pvt_key=self.pvt_key,
                pbc_key=self.pbc_key
            )
            
            print("[BlockTree][replicaID {}] IN process_vote self.pending_vote {} ".format(self.author,len(self.pending_votes[vote_idx])))
            print("[BlockTree][replicaID {}] Formed qc for round {} ".format(self.author, qc))
            return qc
        
        print("[BlockTree][replicaID {}] END process_vote  ".format(self.author))
        diem_logger.info("Could not form qc for vote msg at replica {}. Vote count {} ".format(self.author, len(self.pending_votes[vote_idx])))
        return None

    def generate_block(self,txns,current_round):      
        print("[BlockTree][replicaID {}] START generate_block current_round {} txns {} ".format(self.author,current_round,txns))
  
        new_block = Block(
                                    author=self.author,
                                    roundNo=current_round,
                                    payload=txns,
                                    qc=self.high_qc,
                                    pvt_key=self.pvt_key,
                                    pbc_key=self.pbc_key
                                )   
        print("[BlockTree][replicaID {}] END generate_block current_round {} ".format(self.author,current_round))
        return new_block
        
        ## Creating genesis block for startup 
# compute_block=x.generate_block(1,2)
# print(compute_block)

