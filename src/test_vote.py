
from  certificates.quorum import Quorum
from crypto import Keys as keys

from VoteInfo import VoteInfo as vi
from VoteInfo import VoteInfoSchema 
from BlockTree import BlockTree as bt
from Ledger import Ledger as ld
from Block import Block as blk
from LedgerCommitInfo import LedgerCommitInfo as lci
from Util import Util as util

# from util import max_round_qc,hash
from Util import deserialize, max_round_qc,hash, serialize


class TestSuite:
    def __init__(self):
        pass


    def create_nodes(self):

        blocks = list()
        genesis_voteInfo = vi.VoteInfo(id=0,round_no=0,parent_id=0,parent_round=0,exec_state_id=0)
        print("parent id ",genesis_voteInfo.parent_id)
        print("genesis_voteInfo ",genesis_voteInfo.id)   
        seralized_genesis_voteInfo =  VoteInfoSchema().dumps(genesis_voteInfo)
        # deserialized =  VoteInfoSchema().load(seralized_genesis_voteInfo)
        # print(deserialized)
        print(type(seralized_genesis_voteInfo)," ",seralized_genesis_voteInfo)
        ledger_commit_info = lci.LedgerCommitInfo(commit_state_id=0,vote_info_hash=hash((seralized_genesis_voteInfo)))  
        print("ledger_conmmit_info",ledger_commit_info)
        print("ledger type ",type(ledger_commit_info))
        genesis_qc = QC.QC(vote_info=genesis_voteInfo,ledger_commit_info=ledger_commit_info)
        print("genesis_qc", type(genesis_qc))
        genesis =  blk.Block("genesis",0,"text",genesis_qc,0)

        blocks.append(genesis)

        block1_voteInfo =  vi.VoteInfo(id=1,round_no=1,parent_id=0,parent_round=0,exec_state_id=0)
        print("parent id block1_voteInfo",block1_voteInfo.parent_id)

        seralized_block1_voteInfo =  VoteInfoSchema().dumps(block1_voteInfo)
        ledger_commit_info_1 = lci.LedgerCommitInfo(commit_state_id=1,vote_info_hash=hash((seralized_block1_voteInfo)))  
        block1_qc = QC.QC(vote_info=block1_voteInfo,ledger_commit_info=ledger_commit_info_1) 
        block1 =  blk.Block("validator1",1,"cmd1",block1_qc,1)
        blocks.append(block1)

        block2_voteInfo =  vi.VoteInfo(id=2,round_no=2,parent_id=1,parent_round=1,exec_state_id=0)
        print("parent id,block2_voteInfo ",block2_voteInfo.parent_id)

        seralized_block2_voteInfo =  VoteInfoSchema().dumps(block2_voteInfo)
        ledger_commit_info_2 = lci.LedgerCommitInfo(commit_state_id=0,vote_info_hash=hash((seralized_block2_voteInfo)))  
        block2_qc = QC.QC(vote_info=block2_voteInfo,ledger_commit_info=ledger_commit_info_2) 
        block2 =  blk.Block("validator1",2,"cmd1",block2_qc,2)
        blocks.append(block2)



        block3_voteInfo =  vi.VoteInfo(id=3,round_no=3,parent_id=1,parent_round=2,exec_state_id=0)
        print("parent id,block3_voteInfo ",block3_voteInfo.parent_id)

        seralized_block3_voteInfo =  VoteInfoSchema().dumps(block3_voteInfo)
        ledger_commit_info_3 = lci.LedgerCommitInfo(commit_state_id=0,vote_info_hash=hash((seralized_block3_voteInfo)))  
        block3_qc = QC.QC(vote_info=block3_voteInfo,ledger_commit_info=ledger_commit_info_3) 
        block3 =  blk.Block("validator1",3,"cmd1",block3_qc,3)
        blocks.append(block3)
        return blocks




    def testLedger(self):

        l = ld.Ledger()
        blocks = self.create_nodes()
        for block in blocks:            
            l.speculate(prev_block_id=block.qc.vote_info.parent_id,block_id=block.id,txns=block.payload)
            l.commit(block.id)
        l.print_ledger()

        


        
    def testPendingBlockTree(self):
        blocks=  self.create_nodes()

        pbt = PendingBlockTree()
        for block in blocks:
            print("parent id ",block.qc.vote_info.parent_id)
            pbt.add(block=block,prev_block_id=block.qc.vote_info.parent_id)
        
        for key in pbt.keys():
            print(key,pbt[key],key.id if key!="root" else key)

        pbt.prune(1)
        print("After pruning ")
        for key in pbt.keys():
            print(key,pbt[key],key.id if key!="root" else key)



    def testBlockTree(self):
        blocks=  self.create_nodes()
        bt =  BlockTree(blocks[0].qc)
        for block in blocks:
            bt.execute_and_insert(block)
            bt.process_qc(block.qc)
        
        block_generated =  bt.generate_block("cmd2",2)
        print(block_generated.id,block_generated.roundNo)



    def test_serializers(self):
        v = vi.VoteInfo(1, 2, 3, 4, 5)
        serialed_v = util.serialize(v, VoteInfoSchema())
        ledger = lci.LedgerCommitInfo(1, util.hash(serialed_v))
        serialized_ledger = util.serialize(ledger, lci.LedgerCommitInfoSchema())
        va = util.deserialize(serialed_v, VoteInfoSchema())
        d = util.deserialize(serialized_ledger, lci.LedgerCommitInfoSchema())
        print(type(d._vote_info_hash))
        qc = Quorum.QC(v, ledger)
        print(ledger.vote_info_hash)
        serialized_qc = util.serialize(qc, Quorum.QCSchema())
        print(serialized_qc)
        # serialed_qc = util.serialize(qc, pass)


test =  TestSuite()
# test.testLedger()
test.test_qc_serialize()
test.testLedger()
test.testPendingBlockTree()
test.testBlockTree()
    

# b =  bt.BlockTree()
# print(b.pending_block_tree)
# b.pending_block_tree[10]='test'
# b.pending_block_tree[12]='test12'


# print("block ",b.pending_block_tree)
# b.pending_block_tree.prune(12)
# print("block pruning ",b.pending_block_tree)

# qc_a = quorum.QC(1)
# qc_b = quorum.QC(2)


# y = genkey.GenerateKey(5)
# y.write_config()
# y=quorum.QC("0")
# print(y)

# x = VoteMsg.VoteMsg("hel")
# print(x.ledger_commit_info)
# print(x.signature)
# z=keys.Keys(0)
# print(z.decrypt(x.signature,0))
