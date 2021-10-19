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


        #logger.debug("PendingBlockTree END: init")
        
    def get_node(self,block_id):
        print("get_node for block id {} ".format(block_id))

        return self.cache[block_id]

    def add(self,prev_node_id,block):
        print("Block id {} added to {} ".format(block.id,prev_node_id))
        node =  self.get_node(prev_node_id)
        print("Block {} added to {} ".format(block,prev_node_id))
        node.childNodes[block.id]=Node(prev_node_id,block)
        self.cache[block.id]=node.childNodes[block.id]
    
    def prune(self,id):
        print("PRUNING {}".format(id))
        self.print_cache()
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
        print("block {} ".format(temp.block))

        for i in temp.childNodes.keys():            
            print("parent node : {} childNode: id {} ,node {} ".format(temp.childNodes[i].prev_node_id,i,temp.childNodes[i].block.payload))
            self.helper(temp.childNodes[i])

    def print_nodes(self):
        temp = self.root
        self.helper(temp)
        
    def print_cache(self):
        print("PRINTING CACHE ")
        for i in self.cache.keys():
            print("key {} ,value {} block  {}".format(i,self.cache[i],self.cache[i].block))


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


# g = gk.GenerateKey(5)
# g.write_config()
# k0 = keys.Keys(0)

# genesis_qc , genesis_block =create_genesis_object(k0._private_key,k0._public_key)
# genesis_block =  Block(0,0,"genesis",genesis_qc,k0._private_key,k0._public_key)
# genesis_block.id=0
# pd =  PendingBlockTree(genesis_block)

# block1 =  Block(1,0,"cmd1",genesis_qc,k0._private_key,k0._public_key)
# pd.add(0,block1)
# block2 =  Block(2,0,"cmd2",genesis_qc,k0._private_key,k0._public_key)
# pd.add(0,block2)

# block3=  Block(3,0,"cmd3",genesis_qc,k0._private_key,k0._public_key)
# pd.add(block2.id,block3)

# print("printing node \n\n")
# pd.print_nodes()

# print("printig cache before prunning  \n\n")
# pd.print_cache()

# pd.prune(0)
# print("Cache after prune ")
# pd.print_cache()
# print("printing node after pruning 0  \n\n")
# pd.print_nodes()
# print("size of cache ",pd.cache)


# pd.prune(0)
# print("printing node after pruning 0  \n\n")
# pd.print_nodes()
# print("Cache after prune  \n\n")
# pd.print_cache()



# pd.prune(block3.id)
# print("printing node after pruning 3  \n\n")
# pd.print_nodes()
# print("Cache after prune ")
# pd.print_cache()
