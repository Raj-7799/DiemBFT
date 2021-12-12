import plyvel
import pickle
import BlockTree
import os 
import glob
import shutil
from tabulate import tabulate
import sys
replicaID=[0, 1, 2, 3]
count =  sys.argv[1] if len(sys.argv) > 1 else 4
clean  = sys.argv[2] if len(sys.argv) > 2 else "yes"
replicaID = [ x for x in range(0,int(count))]
# replicaID=[0]
for i in replicaID:
    _db = plyvel.DB('/tmp/diemLedger_{}/'.format(i), create_if_missing=True)
    _db_s = plyvel.DB('/tmp/diemLedger_speculate_{}/'.format(i), create_if_missing=True)
    print("\n\n Commits for replica ", i)
    ledger = []
    
    it = _db.iterator(include_key=False,reverse=True)
    value = next(it)
    block = pickle.loads(value)[1]
   
    while type(block.qc.vote_info.id)!=int and block.qc.vote_info.id!=0:
        # print(block.qc.vote_info.id, block.payload, block.id)
        ledger.append([block.qc.vote_info.id, block.payload, block.id])
        value = _db.get(bytes(str(block.qc.vote_info.id),'utf-8'))
        if value is None:
            break
        block = pickle.loads(value)[1]

    value = _db.get(bytes(str(block.qc.vote_info.id),'utf-8'))
    ledger.append([block.qc.vote_info.id, block.payload, block.id])
    ledger.reverse()
        
    print(tabulate(ledger, headers=["Parent Block ID", "Block transaction", "Block ID"]))
    
    _db.close()


_db.close()
_db.closed
## cleanup 
if clean in ["y","Y","Yes","YES","yes"]:
    print("Cleaning up the ledger files ")
    files=glob.glob('/tmp/diemLedger_*')
    for file in files:
        x = shutil.rmtree(file)