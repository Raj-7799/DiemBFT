from vote import VoteMsg as votemsg
from crypto import GenerateKey as genkey

from crypto import Keys as keys

y = genkey.GenerateKey(5)
y.write_config()
# x = VoteMsg.VoteMsg("hel")
# print(x.ledger_commit_info)
# print(x.signature)
# z=keys.Keys(0)
# print(z.decrypt(x.signature,0))
