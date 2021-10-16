import plyvel
import pickle
import BlockTree
import os 
import glob
import shutil
replicaID=[0, 1, 2, 3]

for i in replicaID:
    _db = plyvel.DB('/tmp/diemLedger_{}/'.format(i), create_if_missing=True)
    print("Commits for replica ", i)
    with _db.iterator() as it:
        for k,v in it:
            #print(k,v)
            print(k,pickle.loads(v))
    
    _db.close()


_db.close()
_db.closed
## cleanup 
print("Cleaning up the ledger files ")
files=glob.glob('/tmp/diemLedger_*')
for file in files:
    x = shutil.rmtree(file)