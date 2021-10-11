
from  certificates.quorum import Quorum
from crypto import Keys as keys
from vote import VoteInfo
from vote import VoteInfo as vi
from vote.VoteInfo import VoteInfoSchema 
from blockchain import BlockTree as bt
from blockchain import Ledger as ld
from blockchain import Block as blk
from blockchain import LedgerCommitInfo as lci
from util import Util as util

# from util import max_round_qc,hash
from util.Util import deserialize, max_round_qc,hash, serialize


class TestSuite:
    def __init__(self):
        pass

    def testLedger(self):
        l = ld.Ledger()
        genesis_voteInfo = vi.VoteInfo(id=0,round_=0,parent_id=0,parent_round=0,exec_state_id=0)
        
        print("genesis_voteInfo ",genesis_voteInfo.id)   
        seralized_genesis_voteInfo =  VoteInfoSchema().dumps(genesis_voteInfo)
        print(type(seralized_genesis_voteInfo)," ",seralized_genesis_voteInfo)
        ledger_commit_info = lci.LedgerCommitInfo(commit_state_id=0,vote_info_hash=hash((seralized_genesis_voteInfo)))  
        print("ledger_conmmit_info",ledger_commit_info)
        print("ledger type ",type(ledger_commit_info))
        genesis_qc = QC.QC(vote_info=genesis_voteInfo,ledger_commit_info=ledger_commit_info)
        print("genesis_qc", type(genesis_qc))
        genesis =  blk.Block("genesis",0,"text",genesis_qc,1)
        print("qc type",type(genesis.qc))
        print("qc ",genesis.qc)

        l.speculate(prev_block_id=genesis.qc.vote_info.parent_id,block_id=genesis.id,txns=genesis.payload)
    
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
