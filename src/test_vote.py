from vote import VoteMsg as votemsg
from crypto import GenerateKey as genkey

from crypto import Keys as keys
from quorum import QC as quorum

from blockchain import BlockTree as bt


from util import max_round_qc

b =  bt.BlockTree()
print(b.pending_block_tree)
b.pending_block_tree[10]='test'
b.pending_block_tree[12]='test12'


print("block ",b.pending_block_tree)
b.pending_block_tree.prune(12)
print("block pruning ",b.pending_block_tree)

qc_a = quorum.QC(1)
qc_b = quorum.QC(2)


# y = genkey.GenerateKey(5)
# y.write_config()
# y=quorum.QC("0")
# print(y)

# x = VoteMsg.VoteMsg("hel")
# print(x.ledger_commit_info)
# print(x.signature)
# z=keys.Keys(0)
# print(z.decrypt(x.signature,0))
