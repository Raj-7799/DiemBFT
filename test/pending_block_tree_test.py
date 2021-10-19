from BlockTree import Block,VoteInfo,QC,LedgerCommitInfo
import GenerateKey as gk
import Keys as keys



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
        return self.cache[block_id]

    def add(self,prev_node_id,block):
        node =  self.get_node(prev_node_id)
        node.childNodes[block.id]=Node(prev_node_id,block)
        self.cache[block.id]=node.childNodes[block.id]
    
    def prune(self,id):
        curr_node =  self.get_node(id)
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
        

    def helper(self,temp):
        if temp is None:
            return

        for i in temp.childNodes.keys():            
            self.helper(temp.childNodes[i])

    def print_nodes(self):
        temp = self.root
        self.helper(temp)
        
    def print_cache(self):
        for i in self.cache.keys():
            print("key {} ,value {} block  {}".format(i,self.cache[i],self.cache[i].block))


## Creating genesis block for startup 
def create_genesis_object(pvt_key, pbc_key):
    genesis_voteInfo = VoteInfo(id=0,roundNo=0,parent_id=0,parent_round=0,exec_state_id=0)
    ledger_commit_info = LedgerCommitInfo(commit_state_id=0,vote_info=genesis_voteInfo)  
    
    genesis_qc = QC(vote_info=genesis_voteInfo,ledger_commit_info=ledger_commit_info, votes=[], author=0, pvt_key=pvt_key, pbc_key=pbc_key)        
    genesis_block =  Block(0, 0, "genesis",genesis_qc, pvt_key, pbc_key)
    genesis_block.id = 0

    return genesis_qc , genesis_block
