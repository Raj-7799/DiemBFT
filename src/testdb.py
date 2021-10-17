import plyvel
import pickle
import BlockTree
import os 
import glob
import shutil
from tabulate import tabulate

replicaID=[0, 1, 2, 3]

for i in replicaID:
    _db = plyvel.DB('/tmp/diemLedger_{}/'.format(i), create_if_missing=True)
    _db_s = plyvel.DB('/tmp/diemLedger_speculate_{}/'.format(i), create_if_missing=True)
    print("\n\n Commits for replica ", i)
    ledger = []
    with _db.iterator() as it:
        for k,v in it:
            block = pickle.loads(v)[1]
            ledger.append([block.qc.vote_info.id, block.payload, block.id])
    
    ledger.sort(key=lambda x: x[1].payload)

    print(tabulate(ledger, headers=["Parent Block ID", "Block transaction", "Block ID"]))
    
    _db.close()


_db.close()
_db.closed
## cleanup 
print("Cleaning up the ledger files ")
files=glob.glob('/tmp/diemLedger_*')
for file in files:
    x = shutil.rmtree(file)