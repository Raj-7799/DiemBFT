import mempool 
import client_request as cr
from GenerateKey import GenerateKey
from Keys import Keys



GenerateKey(2).write_config()
m = mempool.MemPool()
k = Keys(0)
a = cr.ClientRequest("a", "def", k.private_key)
b = cr.ClientRequest("b", "def", k.private_key)
c = cr.ClientRequest("c", "def", k.private_key)
d = cr.ClientRequest("d", "def", k.private_key)
e = cr.ClientRequest("e", "def", k.private_key)

m.insert_command(a)
print(m)
m.insert_command(b)
m.insert_command(c)
m.markState(b)
m.delete_command(c)
print(m)

